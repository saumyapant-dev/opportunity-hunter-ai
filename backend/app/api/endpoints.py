"""FastAPI REST API endpoints for Opportunity Hunter AI."""
import os
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid
import asyncio

from fastapi import APIRouter, HTTPException, BackgroundTasks, Query, status
from pydantic import BaseModel, Field

from ..models.opportunity import (
    Opportunity,
    OpportunityCreate,
    OpportunityUpdate,
    OpportunityStatus,
    OpportunityType,
    VerificationStatus,
    ResearchRequest,
    ResearchRun,
    ResearchRunStatus,
    UserPreferences,
)
from ..database.db import (
    save_opportunity,
    get_opportunity,
    list_opportunities,
    update_opportunity,
    delete_opportunity,
    create_research_run,
    update_research_run,
    get_research_run,
    get_latest_research_run,
    get_preferences,
    save_preferences,
    get_dashboard_stats,
)
from ..services.deduplication import process_and_deduplicate_opportunities, normalize_url
from ..services.n8n_client import send_research_to_n8n, check_n8n_health
from ..agents.browser_researcher import execute_research, get_llm_status, get_browser_status

logger = logging.getLogger(__name__)
router = APIRouter()

# Keep track of last received n8n webhook event for diagnostics
_last_n8n_event: Optional[Dict[str, Any]] = None


async def _run_research_background(run_id: str, request: ResearchRequest):
    """Background task to execute research and persist deduplicated results."""
    try:
        update_research_run(run_id, status=ResearchRunStatus.RUNNING)
        logger.info(f"Starting research execution for run_id={run_id} (mode={request.mode})")

        opportunities = await execute_research(request)
        saved_items, new_count, dup_count = process_and_deduplicate_opportunities(opportunities)

        completed_at = datetime.now(timezone.utc).isoformat()
        update_research_run(
            run_id=run_id,
            status=ResearchRunStatus.COMPLETED,
            completed_at=completed_at,
            results_count=len(saved_items),
        )
        logger.info(
            f"Completed run_id={run_id}: {len(saved_items)} total opportunities ({new_count} new, {dup_count} duplicate)."
        )
    except Exception as e:
        logger.error(f"Failed research execution for run_id={run_id}: {e}", exc_info=True)
        completed_at = datetime.now(timezone.utc).isoformat()
        update_research_run(
            run_id=run_id,
            status=ResearchRunStatus.FAILED,
            completed_at=completed_at,
            results_count=0,
            error_message=str(e),
        )


# --- 1. Health & Status Endpoints ---

@router.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint reporting API and database operational status."""
    return {
        "status": "healthy",
        "service": "opportunity-hunter-backend",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "database": "sqlite",
    }


@router.get("/api/workflows/status", tags=["Workflows"])
async def get_workflow_and_system_status():
    """Diagnostic status for n8n integration, Browser Use agent, LLM configuration, and database."""
    n8n_info = await check_n8n_health()
    llm_info = get_llm_status()
    browser_info = get_browser_status()
    stats = get_dashboard_stats()

    return {
        "n8n": {
            **n8n_info,
            "last_event": _last_n8n_event,
        },
        "browser_agent": browser_info,
        "llm": llm_info,
        "system": {
            "total_opportunities": stats["total_opportunities"],
            "last_run": stats["last_research_run"],
        },
    }


@router.get("/api/dashboard/stats", tags=["Dashboard"])
async def get_dashboard_summary():
    """Aggregated statistics for the main dashboard view."""
    return get_dashboard_stats()


# --- 2. Research Endpoints ---

class ResearchResponse(BaseModel):
    run_id: str
    status: ResearchRunStatus
    mode: str
    message: str
    orchestrator: str


@router.post("/api/research", response_model=ResearchResponse, status_code=status.HTTP_202_ACCEPTED, tags=["Research"])
async def trigger_research(
    request: ResearchRequest,
    background_tasks: BackgroundTasks,
    use_n8n: Optional[bool] = Query(None, description="Force n8n or direct runner"),
):
    """
    Trigger an opportunity discovery research run.
    Validates criteria and routes through n8n webhook or internal background runner.
    """
    run_id = str(uuid.uuid4())
    run = ResearchRun(
        id=run_id,
        status=ResearchRunStatus.RUNNING,
        started_at=datetime.now(timezone.utc).isoformat(),
        mode=request.mode,
        request_params=request.model_dump(),
    )
    create_research_run(run)

    # Determine orchestration path
    n8n_enabled = os.getenv("N8N_INTEGRATION_ENABLED", "false").lower() in ("true", "1", "yes")
    should_use_n8n = use_n8n if use_n8n is not None else n8n_enabled

    if should_use_n8n:
        n8n_result = await send_research_to_n8n(run_id=run_id, request=request)
        if n8n_result.get("success"):
            return ResearchResponse(
                run_id=run_id,
                status=ResearchRunStatus.RUNNING,
                mode=request.mode,
                message="Research request dispatched to n8n workflow for orchestration.",
                orchestrator="n8n",
            )
        else:
            logger.warning(
                f"n8n dispatch failed ({n8n_result.get('error')}). Falling back to internal runner."
            )

    # Execute directly via background tasks
    background_tasks.add_task(_run_research_background, run_id, request)
    return ResearchResponse(
        run_id=run_id,
        status=ResearchRunStatus.RUNNING,
        mode=request.mode,
        message=f"Research started ({request.mode} mode). Monitoring progress via /api/research/{run_id}",
        orchestrator="direct",
    )


@router.get("/api/research/{run_id}", response_model=ResearchRun, tags=["Research"])
async def get_run_status(run_id: str):
    """Retrieve execution status, timestamp, and results count for a research run."""
    run = get_research_run(run_id)
    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Research run with ID '{run_id}' not found.",
        )
    return run


# --- 3. Browser Use Direct Execution (used by n8n HTTP Request node) ---

class AgentExecutionRequest(BaseModel):
    run_id: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    opportunity_types: List[str] = Field(default_factory=list)
    location: str = "Remote"
    experience: str = "Beginner"
    keywords: List[str] = Field(default_factory=list)
    preferred_domains: List[str] = Field(default_factory=list)
    max_results: int = 10
    mode: str = "mock"


@router.post("/api/browser-use/execute", tags=["Browser Agent"])
async def execute_browser_agent_direct(payload: AgentExecutionRequest):
    """
    Direct invocation of the Browser Use agent.
    Called by n8n workflow to perform web discovery and extract structured listings.
    """
    req = ResearchRequest(
        skills=payload.skills,
        opportunity_types=payload.opportunity_types,
        location=payload.location,
        experience=payload.experience,
        keywords=payload.keywords,
        preferred_domains=payload.preferred_domains,
        max_results=payload.max_results,
        mode=payload.mode,
    )
    opportunities = await execute_research(req)
    return {
        "run_id": payload.run_id or str(uuid.uuid4()),
        "count": len(opportunities),
        "opportunities": [o.model_dump() for o in opportunities],
    }


# --- 4. Opportunity Catalog Endpoints ---

@router.get("/api/opportunities", response_model=List[Opportunity], tags=["Opportunities"])
async def get_opportunities(
    type: Optional[str] = Query(None, description="Filter by type (internship, hackathon, research, job)"),
    status: Optional[str] = Query(None, description="Filter by status (new, saved, interested, applied, rejected)"),
    search: Optional[str] = Query(None, description="Search term in title, organization, or skills"),
    remote_only: Optional[bool] = Query(None, description="Filter remote only"),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    """List discovered opportunities with rich filtering, search, and pagination."""
    return list_opportunities(
        type_filter=type,
        status_filter=status,
        search=search,
        remote_only=remote_only,
        limit=limit,
        offset=offset,
    )


@router.get("/api/opportunities/{id}", response_model=Opportunity, tags=["Opportunities"])
async def get_single_opportunity(id: str):
    """Retrieve full details of an opportunity by ID."""
    opp = get_opportunity(id)
    if not opp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Opportunity with ID '{id}' not found.",
        )
    return opp


@router.patch("/api/opportunities/{id}", response_model=Opportunity, tags=["Opportunities"])
async def modify_opportunity(id: str, updates: OpportunityUpdate):
    """Update opportunity attributes (e.g. status: saved, applied, interested, or notes)."""
    updated = update_opportunity(id, updates)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Opportunity with ID '{id}' not found.",
        )
    return updated


@router.delete("/api/opportunities/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Opportunities"])
async def remove_opportunity(id: str):
    """Delete an opportunity from the database."""
    success = delete_opportunity(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Opportunity with ID '{id}' not found.",
        )
    return None


# --- 5. User Preferences Endpoints ---

@router.get("/api/preferences", response_model=UserPreferences, tags=["Preferences"])
async def fetch_preferences():
    """Retrieve saved user research preferences and notification configurations."""
    return get_preferences()


@router.put("/api/preferences", response_model=UserPreferences, tags=["Preferences"])
async def update_user_preferences(prefs: UserPreferences):
    """Save updated default skills, target types, notification email, and LLM preferences."""
    return save_preferences(prefs)


# --- 6. n8n Inbound Webhook Receiver ---

class N8nResultsPayload(BaseModel):
    run_id: Optional[str] = None
    opportunities: List[Dict[str, Any]] = Field(default_factory=list)
    status: Optional[str] = "completed"
    error_message: Optional[str] = None


@router.post("/api/webhooks/n8n/results", status_code=status.HTTP_200_OK, tags=["Webhooks"])
async def receive_n8n_results(payload: N8nResultsPayload):
    """
    Webhook receiver endpoint invoked by n8n workflow after completing opportunity research.
    Deduplicates results, persists them to SQLite, and updates the research run state.
    """
    global _last_n8n_event
    _last_n8n_event = {
        "received_at": datetime.now(timezone.utc).isoformat(),
        "run_id": payload.run_id,
        "count": len(payload.opportunities),
        "status": payload.status,
    }
    logger.info(f"Received n8n webhook callback for run_id={payload.run_id} ({len(payload.opportunities)} items)")

    incoming_opportunities: List[Opportunity] = []
    now = datetime.now(timezone.utc).isoformat()

    for item in payload.opportunities:
        try:
            # Map type safely
            raw_type = str(item.get("type", "internship")).lower()
            if "hack" in raw_type:
                opp_type = OpportunityType.HACKATHON
            elif "research" in raw_type:
                opp_type = OpportunityType.RESEARCH
            elif "job" in raw_type:
                opp_type = OpportunityType.JOB
            else:
                opp_type = OpportunityType.INTERNSHIP

            opp = Opportunity(
                id=item.get("id") or str(uuid.uuid4()),
                title=item.get("title", "Untitled Opportunity"),
                organization=item.get("organization", "Unknown Organization"),
                type=opp_type,
                description=item.get("description", "No description provided."),
                required_skills=item.get("required_skills") or [],
                location=item.get("location", "Remote"),
                remote=bool(item.get("remote", True)),
                deadline=item.get("deadline"),
                application_url=item.get("application_url", item.get("source_url", "https://example.com")),
                source_url=item.get("source_url", "https://example.com"),
                discovered_at=item.get("discovered_at") or now,
                status=OpportunityStatus.NEW,
                verification_status=VerificationStatus.VERIFIED if item.get("verification_status") == "verified" else VerificationStatus.UNVERIFIED,
            )
            incoming_opportunities.append(opp)
        except Exception as e:
            logger.warning(f"Error parsing item from n8n: {e}")

    saved_items, new_count, dup_count = process_and_deduplicate_opportunities(incoming_opportunities)

    if payload.run_id:
        update_research_run(
            run_id=payload.run_id,
            status=ResearchRunStatus.COMPLETED if payload.status == "completed" else ResearchRunStatus.FAILED,
            completed_at=datetime.now(timezone.utc).isoformat(),
            results_count=len(saved_items),
            error_message=payload.error_message,
        )

    return {
        "success": True,
        "run_id": payload.run_id,
        "processed_count": len(incoming_opportunities),
        "new_saved": new_count,
        "duplicates_updated": dup_count,
    }

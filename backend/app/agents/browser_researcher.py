"""Browser Use Web AI Research Agent integration."""
import os
from pathlib import Path
import json
import logging
import asyncio
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

# Ensure browser use config dir is set before importing browser_use
project_root = Path(__file__).resolve().parent.parent.parent.parent
default_config_dir = project_root / ".browseruse"
default_config_dir.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("BROWSER_USE_CONFIG_DIR", str(default_config_dir))

from ..models.opportunity import (
    ResearchRequest,
    Opportunity,
    OpportunityType,
    OpportunityStatus,
    VerificationStatus,
    OpportunityListOutput,
    ExtractedOpportunity,
)

logger = logging.getLogger(__name__)


def get_llm_status() -> Dict[str, Any]:
    """Inspect current LLM provider configuration safely without exposing secrets."""
    provider = os.getenv("LLM_PROVIDER", "mock").lower()
    openrouter_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    model = os.getenv("LLM_MODEL", "meta-llama/llama-3.3-70b-instruct")

    is_configured = False
    if provider == "openrouter":
        is_configured = bool(openrouter_key)
    elif provider == "openai":
        is_configured = bool(openai_key)
    elif provider == "mock":
        is_configured = True

    return {
        "provider": provider,
        "configured": is_configured,
        "model": model,
        "has_openrouter_key": bool(openrouter_key),
        "has_openai_key": bool(openai_key),
        "mode_available": ["mock", "openrouter", "openai"],
    }


def get_browser_status() -> Dict[str, Any]:
    """Inspect Playwright and Browser Use availability."""
    config_dir = os.getenv("BROWSER_USE_CONFIG_DIR", str(default_config_dir))
    headless = os.getenv("BROWSER_USE_HEADLESS", "true").lower() in ("true", "1", "yes")
    return {
        "browser_engine": "Browser-Use (Playwright Chromium)",
        "headless": headless,
        "config_dir": config_dir,
        "available": True,
    }


def _generate_mock_opportunities(request: ResearchRequest) -> List[Opportunity]:
    """
    Generate realistic, high-fidelity mock opportunities customized to the user's
    exact query parameters (skills, types, location, keywords) for instant verification
    without consuming LLM quota or requiring external network.
    """
    results: List[Opportunity] = []
    types = request.opportunity_types or ["internship", "hackathon"]
    primary_skills = request.skills or ["Python", "JavaScript", "React"]
    location = request.location or "Remote"
    experience = request.experience or "Beginner"

    # Template banks for realistic student opportunities
    templates = [
        {
            "org": "AI Frontier Labs",
            "title_fmt": "Generative AI Research Intern ({experience})",
            "type": OpportunityType.INTERNSHIP,
            "skills": [primary_skills[0] if primary_skills else "Python", "PyTorch", "HuggingFace"],
            "desc": f"Conduct applied research on multimodal LLM reasoning and agent benchmarks. Mentored by senior researchers. Open to {experience.lower()} candidates.",
            "url_slug": "ai-frontier-intern",
            "source": "https://careers.aifrontierlabs.io/openings",
            "deadline_offset_days": 30,
        },
        {
            "org": "OpenDev Community",
            "title_fmt": "Global AI & Open Source Hackathon 2026",
            "type": OpportunityType.HACKATHON,
            "skills": primary_skills[:3] or ["Python", "React", "APIs"],
            "desc": "A 48-hour worldwide virtual hackathon building autonomous workflow agents and modern web applications. $50,000 prize pool and incubator interviews.",
            "url_slug": "global-ai-hackathon",
            "source": "https://devpost.com/hackathons/global-ai-2026",
            "deadline_offset_days": 14,
        },
        {
            "org": "Nexus Health Robotics",
            "title_fmt": "Software Engineering Co-Op / Intern",
            "type": OpportunityType.INTERNSHIP,
            "skills": [s for s in primary_skills if s in ["Python", "Java", "C++", "React"]] or ["Python", "React"],
            "desc": f"Build responsive clinician dashboards and microservice pipelines. Perfect for {experience.lower()} developers looking for real-world production experience.",
            "url_slug": "nexus-health-coop",
            "source": "https://jobs.lever.co/nexushealth/eng-intern",
            "deadline_offset_days": 21,
        },
        {
            "org": "Quantum Dynamics Institute",
            "title_fmt": "Undergraduate Research Fellowship in Machine Learning",
            "type": OpportunityType.RESEARCH,
            "skills": ["Python", "Data Structures", "Machine Learning"],
            "desc": "Funded 12-week summer research fellowship studying neural network interpretability and graph algorithms. Stipend included.",
            "url_slug": "quantum-dynamics-fellowship",
            "source": "https://quantumdynamics.edu/fellowships",
            "deadline_offset_days": 45,
        },
        {
            "org": "CloudScale Systems",
            "title_fmt": "Junior Full Stack Engineer ({location})",
            "type": OpportunityType.JOB,
            "skills": ["JavaScript", "React", "SQL", "FastAPI"],
            "desc": "Entry-level full stack position developing high-throughput customer portals. Structured onboarding and engineering mentorship provided.",
            "url_slug": "cloudscale-junior-engineer",
            "source": "https://www.workatastartup.com/companies/cloudscale",
            "deadline_offset_days": 60,
        },
        {
            "org": "FinTech Innovations",
            "title_fmt": "Algorithmic Trading & Backend Intern",
            "type": OpportunityType.INTERNSHIP,
            "skills": ["Python", "SQL", "Data Structures"],
            "desc": "Develop real-time data ingestion pipelines and backtesting frameworks. Fast-paced collaborative team environment.",
            "url_slug": "fintech-algo-intern",
            "source": "https://fintechinnovations.com/careers",
            "deadline_offset_days": 18,
        },
        {
            "org": "Web3 Builders Guild",
            "title_fmt": "Smart Contract & UI Builder Hackathon",
            "type": OpportunityType.HACKATHON,
            "skills": ["React", "JavaScript", "Rust"],
            "desc": "Build next-generation decentralized applications and web tools. Mentors available throughout the sprint.",
            "url_slug": "web3-builders-hackathon",
            "source": "https://devpost.com/hackathons/web3-builders",
            "deadline_offset_days": 10,
        },
        {
            "org": "Cognitive Science Consortium",
            "title_fmt": "Research Assistant - Computational Linguistics",
            "type": OpportunityType.RESEARCH,
            "skills": ["Python", "Machine Learning", "NLP"],
            "desc": "Collaborate on dataset curation and evaluation of multi-turn dialogue models. Co-authorship opportunities for publication.",
            "url_slug": "cogsci-nlp-research",
            "source": "https://cogsci-consortium.org/openings",
            "deadline_offset_days": 35,
        },
    ]

    selected_templates = []
    # Filter or match by requested opportunity types
    type_strings = [t.lower() for t in types]
    for tmpl in templates:
        if tmpl["type"].value in type_strings:
            selected_templates.append(tmpl)

    if not selected_templates:
        selected_templates = templates

    now = datetime.now(timezone.utc)
    for i, tmpl in enumerate(selected_templates[: request.max_results]):
        deadline_date = (
            datetime.fromtimestamp(now.timestamp() + tmpl["deadline_offset_days"] * 86400, timezone.utc)
            .strftime("%Y-%m-%d")
        )
        opp_id = str(uuid.uuid4())
        app_url = f"{tmpl['source']}/apply/{tmpl['url_slug']}?ref=opphunter_{opp_id[:8]}"

        opp = Opportunity(
            id=opp_id,
            title=tmpl["title_fmt"].format(experience=experience, location=location),
            organization=tmpl["org"],
            type=tmpl["type"],
            description=f"[MOCK RESEARCH RESULT] {tmpl['desc']}",
            required_skills=tmpl["skills"],
            location=location,
            remote=True if "remote" in location.lower() else False,
            deadline=deadline_date,
            application_url=app_url,
            source_url=tmpl["source"],
            discovered_at=now.isoformat(),
            status=OpportunityStatus.NEW,
            verification_status=VerificationStatus.UNVERIFIED,
        )
        results.append(opp)

    return results


async def _run_browser_use_live(request: ResearchRequest) -> List[Opportunity]:
    """
    Execute real web research using Browser Use and Playwright.
    Navigates to configured discovery platforms, queries them, extracts listings,
    and returns structured Opportunity models.
    """
    from browser_use import Agent, Browser, ChatOpenRouter, ChatOpenAI

    provider = os.getenv("LLM_PROVIDER", "openrouter").lower()
    model_name = os.getenv("LLM_MODEL", "meta-llama/llama-3.3-70b-instruct")
    openrouter_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    base_url = os.getenv("LLM_BASE_URL", "https://openrouter.ai/api/v1")
    headless = os.getenv("BROWSER_USE_HEADLESS", "true").lower() in ("true", "1", "yes")

    # Select LLM
    if provider == "openrouter":
        if not openrouter_key:
            raise ValueError("OPENROUTER_API_KEY is not configured.")
        llm = ChatOpenRouter(
            model=model_name,
            api_key=openrouter_key,
            base_url=base_url,
        )
    elif provider == "openai":
        if not openai_key:
            raise ValueError("OPENAI_API_KEY is not configured.")
        llm = ChatOpenAI(
            model=model_name,
            api_key=openai_key,
            base_url=base_url if "openai.com" not in base_url else None,
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")

    # Build target prompt
    skills_str = ", ".join(request.skills) if request.skills else "Software Engineering"
    types_str = ", ".join(request.opportunity_types) if request.opportunity_types else "Internships, Hackathons"
    keywords_str = ", ".join(request.keywords) if request.keywords else ""

    target_domains = request.preferred_domains or ["news.ycombinator.com/jobs", "devpost.com/hackathons"]
    domains_str = ", ".join(target_domains)

    prompt = (
        f"You are Opportunity Hunter AI. Find up to {request.max_results} genuine student opportunities.\n"
        f"Desired types: {types_str}.\n"
        f"Key skills: {skills_str}.\n"
        f"Location: {request.location}.\n"
        f"Experience Level: {request.experience}.\n"
        f"Keywords: {keywords_str}.\n"
        f"Recommended sites: {domains_str}.\n\n"
        f"Instructions:\n"
        f"1. Navigate to relevant opportunity boards (e.g. https://news.ycombinator.com/jobs or https://devpost.com/hackathons).\n"
        f"2. Inspect available listings that match the criteria.\n"
        f"3. Extract title, organization, type, brief description, required skills, location, application URL, and source URL.\n"
        f"4. If a deadline is explicitly listed, record it; otherwise set deadline to null. NEVER invent deadlines or application links.\n"
        f"5. Return the structured results in the output schema."
    )

    browser = Browser(headless=headless)
    agent = Agent(
        task=prompt,
        llm=llm,
        browser=browser,
        output_model_schema=OpportunityListOutput,
        max_failures=3,
        step_timeout=120,
    )

    max_steps = int(os.getenv("BROWSER_USE_MAX_STEPS", "20"))
    history = await agent.run(max_steps=max_steps)

    extracted_items: List[ExtractedOpportunity] = []
    try:
        structured = history.get_structured_output(OpportunityListOutput)
        if structured and structured.opportunities:
            extracted_items = structured.opportunities
    except Exception as e:
        logger.warning(f"Could not parse structured output directly: {e}")

    opportunities: List[Opportunity] = []
    now = datetime.now(timezone.utc).isoformat()

    for item in extracted_items:
        # Map string type to enum safely
        raw_type = item.type.lower()
        if "hack" in raw_type:
            opp_type = OpportunityType.HACKATHON
        elif "research" in raw_type:
            opp_type = OpportunityType.RESEARCH
        elif "job" in raw_type:
            opp_type = OpportunityType.JOB
        else:
            opp_type = OpportunityType.INTERNSHIP

        opp = Opportunity(
            id=str(uuid.uuid4()),
            title=item.title,
            organization=item.organization,
            type=opp_type,
            description=item.description,
            required_skills=item.required_skills,
            location=item.location or request.location,
            remote=item.remote,
            deadline=item.deadline,
            application_url=item.application_url,
            source_url=item.source_url,
            discovered_at=now,
            status=OpportunityStatus.NEW,
            verification_status=VerificationStatus.VERIFIED if item.verification_status == "verified" else VerificationStatus.UNVERIFIED,
        )
        opportunities.append(opp)

    return opportunities


async def execute_research(request: ResearchRequest) -> List[Opportunity]:
    """
    Main entry point for research execution.
    Dispatches to Mock mode or Live Browser Use agent based on request mode and credentials.
    """
    mode = (request.mode or os.getenv("LLM_PROVIDER", "mock")).lower()

    if mode == "mock":
        logger.info("Executing research in MOCK mode (zero API credit usage).")
        # Add slight async delay to simulate realistic network search
        await asyncio.sleep(1.0)
        return _generate_mock_opportunities(request)

    # Live mode requested
    logger.info(f"Executing LIVE Browser Use research (provider: {os.getenv('LLM_PROVIDER')}).")
    try:
        return await _run_browser_use_live(request)
    except Exception as e:
        logger.error(f"Live Browser Use research encountered error: {e}. Falling back to mock generator.", exc_info=True)
        # Resilient fallback so users get informative results while debugging browser setup
        mock_results = _generate_mock_opportunities(request)
        for r in mock_results:
            r.description = f"[FALLBACK RESULT - LIVE RUN FAILED: {str(e)[:120]}] {r.description}"
        return mock_results

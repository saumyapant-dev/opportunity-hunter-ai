"""n8n webhook communication and health integration service."""
import os
import logging
from typing import Dict, Any, List, Optional
import httpx

from ..models.opportunity import ResearchRequest, Opportunity

logger = logging.getLogger(__name__)

DEFAULT_N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook/opportunity-research")
N8N_API_KEY = os.getenv("N8N_API_KEY", "")


async def check_n8n_health() -> Dict[str, Any]:
    """Check connectivity to the n8n instance and webhook endpoint."""
    webhook_url = os.getenv("N8N_WEBHOOK_URL", DEFAULT_N8N_WEBHOOK_URL)
    enabled = os.getenv("N8N_INTEGRATION_ENABLED", "false").lower() in ("true", "1", "yes")

    # Parse base host for general n8n health
    base_url = webhook_url.split("/webhook")[0] if "/webhook" in webhook_url else "http://localhost:5678"

    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            resp = await client.get(f"{base_url}/healthz")
            if resp.status_code == 200:
                return {
                    "connected": True,
                    "status": "online",
                    "webhook_url": webhook_url,
                    "integration_enabled": enabled,
                    "message": "n8n service is healthy and reachable.",
                }
    except Exception as e:
        logger.debug(f"n8n /healthz ping failed: {e}")

    # Fallback check on base URL
    try:
        async with httpx.AsyncClient(timeout=1.5) as client:
            resp = await client.get(base_url)
            if resp.status_code in (200, 301, 302, 401, 403):
                return {
                    "connected": True,
                    "status": "online",
                    "webhook_url": webhook_url,
                    "integration_enabled": enabled,
                    "message": "n8n server is responding.",
                }
    except Exception:
        pass

    return {
        "connected": False,
        "status": "offline",
        "webhook_url": webhook_url,
        "integration_enabled": enabled,
        "message": "n8n server is not reachable at configured URL. (Start n8n with 'npx n8n' to enable live workflows).",
    }


async def send_research_to_n8n(run_id: str, request: ResearchRequest) -> Dict[str, Any]:
    """Forward a research request to n8n webhook trigger."""
    webhook_url = os.getenv("N8N_WEBHOOK_URL", DEFAULT_N8N_WEBHOOK_URL)
    payload = {
        "run_id": run_id,
        "skills": request.skills,
        "opportunity_types": request.opportunity_types,
        "location": request.location,
        "experience": request.experience,
        "keywords": request.keywords,
        "preferred_domains": request.preferred_domains,
        "max_results": request.max_results,
        "mode": request.mode,
    }

    headers = {"Content-Type": "application/json"}
    if N8N_API_KEY:
        headers["X-N8N-API-KEY"] = N8N_API_KEY

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(webhook_url, json=payload, headers=headers)
            if response.status_code in (200, 201, 202):
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "response": response.text[:200],
                }
            return {
                "success": False,
                "status_code": response.status_code,
                "error": f"n8n returned status {response.status_code}: {response.text[:200]}",
            }
    except httpx.ConnectError:
        return {
            "success": False,
            "error": f"Could not connect to n8n webhook at {webhook_url}. Is n8n running?",
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error dispatching to n8n: {str(e)}",
        }

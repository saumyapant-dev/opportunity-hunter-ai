"""Services package for Opportunity Hunter AI."""
from .deduplication import normalize_url, process_and_deduplicate_opportunities
from .n8n_client import send_research_to_n8n, check_n8n_health

__all__ = [
    "normalize_url",
    "process_and_deduplicate_opportunities",
    "send_research_to_n8n",
    "check_n8n_health",
]

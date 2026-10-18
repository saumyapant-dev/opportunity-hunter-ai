"""Deduplication and URL normalization service for opportunities."""
import re
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from typing import List, Tuple, Optional
from datetime import datetime, timezone

from ..models.opportunity import Opportunity, OpportunityStatus, VerificationStatus
from ..database.db import find_duplicate, save_opportunity, get_opportunity

# Tracking parameters to strip
TRACKING_PARAMS = {
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_term",
    "utm_content",
    "ref",
    "source",
    "fbclid",
    "gclid",
    "trk",
    "msclkid",
    "mc_eid",
    "gh_src",
    "_hsenc",
    "_hsmi",
    "si",
    "src",
}


def normalize_url(raw_url: str) -> str:
    """Normalize URLs by stripping tracking query params, fragments, and standardizing host/path."""
    if not raw_url:
        return ""

    parsed = urlparse(raw_url.strip())
    scheme = parsed.scheme.lower() or "https"
    netloc = parsed.netloc.lower()

    # Strip default port if present
    if netloc.endswith(":80"):
        netloc = netloc[:-3]
    elif netloc.endswith(":443"):
        netloc = netloc[:-4]

    # Normalize path (remove duplicate slashes and trailing slash if not root)
    path = re.sub(r"/+", "/", parsed.path)
    if len(path) > 1 and path.endswith("/"):
        path = path[:-1]

    # Filter out tracking query parameters
    query_params = parse_qsl(parsed.query, keep_blank_values=False)
    filtered_params = [
        (k, v) for k, v in query_params if k.lower() not in TRACKING_PARAMS
    ]
    # Sort remaining parameters for determinism
    filtered_params.sort(key=lambda x: x[0])
    query = urlencode(filtered_params)

    # Reconstruct URL without fragment
    normalized = urlunparse((scheme, netloc, path, parsed.params, query, ""))
    return normalized


def normalize_text(text: str) -> str:
    """Normalize text for fuzzy matching by lowercasing and removing punctuation/common corporate suffixes."""
    if not text:
        return ""
    cleaned = text.lower().strip()
    cleaned = re.sub(r"[^\w\s]", "", cleaned)
    # Remove common organization suffixes
    for suffix in ["inc", "llc", "ltd", "corp", "corporation", "technologies", "tech", "labs", "lab"]:
        cleaned = re.sub(rf"\b{suffix}\b", "", cleaned)
    return re.sub(r"\s+", " ", cleaned).strip()


def process_and_deduplicate_opportunities(
    opportunities: List[Opportunity],
) -> Tuple[List[Opportunity], int, int]:
    """
    Process incoming opportunity list:
    - Normalizes URLs
    - Identifies duplicates against existing database records
    - Updates timestamps on duplicates without overwriting user status
    - Persists new records
    Returns (saved_or_updated_opportunities, new_count, duplicate_count)
    """
    results: List[Opportunity] = []
    new_count = 0
    duplicate_count = 0

    # Also keep track of duplicates within the same batch
    seen_in_batch = set()

    for opp in opportunities:
        norm_app_url = normalize_url(opp.application_url)
        norm_title = normalize_text(opp.title)
        norm_org = normalize_text(opp.organization)

        batch_key = (norm_app_url or f"{norm_title}::{norm_org}")
        if batch_key in seen_in_batch:
            duplicate_count += 1
            continue
        seen_in_batch.add(batch_key)

        existing = find_duplicate(
            normalized_url=norm_app_url,
            title=opp.title,
            organization=opp.organization,
        )

        if existing:
            duplicate_count += 1
            # Refresh discovered timestamp to show it was re-verified/seen again
            existing.discovered_at = datetime.now(timezone.utc).isoformat()
            if opp.verification_status == VerificationStatus.VERIFIED:
                existing.verification_status = VerificationStatus.VERIFIED
            # Keep the existing user status! (e.g. if saved or applied, never reset to new)
            save_opportunity(existing, normalized_url=norm_app_url)
            results.append(existing)
        else:
            new_count += 1
            if not opp.status:
                opp.status = OpportunityStatus.NEW
            save_opportunity(opp, normalized_url=norm_app_url)
            results.append(opp)

    return results, new_count, duplicate_count

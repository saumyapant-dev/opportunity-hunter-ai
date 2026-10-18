"""SQLite persistent storage service for Opportunity Hunter AI."""
import sqlite3
import json
import os
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

from ..models.opportunity import (
    Opportunity,
    OpportunityCreate,
    OpportunityUpdate,
    OpportunityType,
    OpportunityStatus,
    VerificationStatus,
    ResearchRun,
    ResearchRunStatus,
    UserPreferences,
)

DEFAULT_DB_PATH = os.getenv("DATABASE_PATH", "backend/data/opportunities.db")


def get_db_path() -> Path:
    db_path = Path(os.getenv("DATABASE_PATH", DEFAULT_DB_PATH))
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return db_path


def get_db_connection() -> sqlite3.Connection:
    path = get_db_path()
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize SQLite database tables and indexes."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS opportunities (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        organization TEXT NOT NULL,
        type TEXT NOT NULL,
        description TEXT NOT NULL,
        required_skills TEXT NOT NULL,
        location TEXT NOT NULL,
        remote INTEGER NOT NULL,
        deadline TEXT,
        application_url TEXT NOT NULL,
        source_url TEXT NOT NULL,
        discovered_at TEXT NOT NULL,
        status TEXT NOT NULL,
        verification_status TEXT NOT NULL,
        normalized_url TEXT
    )
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_opp_normalized_url ON opportunities(normalized_url);
    """)
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_opp_status ON opportunities(status);
    """)
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_opp_type ON opportunities(type);
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS research_runs (
        id TEXT PRIMARY KEY,
        status TEXT NOT NULL,
        started_at TEXT NOT NULL,
        completed_at TEXT,
        results_count INTEGER NOT NULL DEFAULT 0,
        error_message TEXT,
        mode TEXT NOT NULL DEFAULT 'mock',
        request_params TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_preferences (
        id TEXT PRIMARY KEY DEFAULT 'default',
        data TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


def row_to_opportunity(row: sqlite3.Row) -> Opportunity:
    skills = []
    try:
        skills = json.loads(row["required_skills"])
    except Exception:
        skills = []

    return Opportunity(
        id=row["id"],
        title=row["title"],
        organization=row["organization"],
        type=OpportunityType(row["type"]),
        description=row["description"],
        required_skills=skills,
        location=row["location"],
        remote=bool(row["remote"]),
        deadline=row["deadline"],
        application_url=row["application_url"],
        source_url=row["source_url"],
        discovered_at=row["discovered_at"],
        status=OpportunityStatus(row["status"]),
        verification_status=VerificationStatus(row["verification_status"]),
    )


def save_opportunity(opp: Opportunity, normalized_url: Optional[str] = None) -> Opportunity:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT OR REPLACE INTO opportunities (
            id, title, organization, type, description, required_skills,
            location, remote, deadline, application_url, source_url,
            discovered_at, status, verification_status, normalized_url
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            opp.id,
            opp.title,
            opp.organization,
            opp.type.value,
            opp.description,
            json.dumps(opp.required_skills),
            opp.location,
            1 if opp.remote else 0,
            opp.deadline,
            opp.application_url,
            opp.source_url,
            opp.discovered_at,
            opp.status.value,
            opp.verification_status.value,
            normalized_url or opp.application_url,
        ),
    )
    conn.commit()
    conn.close()
    return opp


def get_opportunity(opp_id: str) -> Optional[Opportunity]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM opportunities WHERE id = ?", (opp_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row_to_opportunity(row)
    return None


def list_opportunities(
    type_filter: Optional[str] = None,
    status_filter: Optional[str] = None,
    search: Optional[str] = None,
    remote_only: Optional[bool] = None,
    limit: int = 100,
    offset: int = 0,
) -> List[Opportunity]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM opportunities WHERE 1=1"
    params: List[Any] = []

    if type_filter:
        query += " AND type = ?"
        params.append(type_filter.lower())
    if status_filter:
        query += " AND status = ?"
        params.append(status_filter.lower())
    if remote_only is not None and remote_only:
        query += " AND remote = 1"
    if search:
        search_pattern = f"%{search.lower()}%"
        query += " AND (LOWER(title) LIKE ? OR LOWER(organization) LIKE ? OR LOWER(description) LIKE ? OR LOWER(required_skills) LIKE ?)"
        params.extend([search_pattern, search_pattern, search_pattern, search_pattern])

    query += " ORDER BY discovered_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [row_to_opportunity(r) for r in rows]


def update_opportunity(opp_id: str, updates: OpportunityUpdate) -> Optional[Opportunity]:
    current = get_opportunity(opp_id)
    if not current:
        return None

    update_dict = updates.model_dump(exclude_unset=True)
    if not update_dict:
        return current

    conn = get_db_connection()
    cursor = conn.cursor()

    set_clauses = []
    params = []
    for key, val in update_dict.items():
        if key == "required_skills" and isinstance(val, list):
            set_clauses.append("required_skills = ?")
            params.append(json.dumps(val))
        elif key == "remote" and isinstance(val, bool):
            set_clauses.append("remote = ?")
            params.append(1 if val else 0)
        elif key in ("type", "status", "verification_status") and hasattr(val, "value"):
            set_clauses.append(f"{key} = ?")
            params.append(val.value)
        else:
            set_clauses.append(f"{key} = ?")
            params.append(val)

    params.append(opp_id)
    cursor.execute(f"UPDATE opportunities SET {', '.join(set_clauses)} WHERE id = ?", params)
    conn.commit()
    conn.close()
    return get_opportunity(opp_id)


def delete_opportunity(opp_id: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM opportunities WHERE id = ?", (opp_id,))
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0


def find_duplicate(normalized_url: str, title: str, organization: str) -> Optional[Opportunity]:
    conn = get_db_connection()
    cursor = conn.cursor()

    # Direct match on normalized URL
    if normalized_url:
        cursor.execute("SELECT * FROM opportunities WHERE normalized_url = ?", (normalized_url,))
        row = cursor.fetchone()
        if row:
            conn.close()
            return row_to_opportunity(row)

    # Fuzzy match on normalized title and organization
    cursor.execute(
        "SELECT * FROM opportunities WHERE LOWER(title) = ? AND LOWER(organization) = ?",
        (title.strip().lower(), organization.strip().lower()),
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        return row_to_opportunity(row)

    return None


def create_research_run(run: ResearchRun) -> ResearchRun:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO research_runs (
            id, status, started_at, completed_at, results_count, error_message, mode, request_params
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            run.id,
            run.status.value,
            run.started_at,
            run.completed_at,
            run.results_count,
            run.error_message,
            run.mode,
            json.dumps(run.request_params) if run.request_params else None,
        ),
    )
    conn.commit()
    conn.close()
    return run


def update_research_run(
    run_id: str,
    status: ResearchRunStatus,
    completed_at: Optional[str] = None,
    results_count: int = 0,
    error_message: Optional[str] = None,
) -> Optional[ResearchRun]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE research_runs
        SET status = ?, completed_at = ?, results_count = ?, error_message = ?
        WHERE id = ?
        """,
        (status.value, completed_at, results_count, error_message, run_id),
    )
    conn.commit()
    cursor.execute("SELECT * FROM research_runs WHERE id = ?", (run_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row_to_research_run(row)
    return None


def row_to_research_run(row: sqlite3.Row) -> ResearchRun:
    params = None
    if row["request_params"]:
        try:
            params = json.loads(row["request_params"])
        except Exception:
            params = None

    return ResearchRun(
        id=row["id"],
        status=ResearchRunStatus(row["status"]),
        started_at=row["started_at"],
        completed_at=row["completed_at"],
        results_count=row["results_count"],
        error_message=row["error_message"],
        mode=row["mode"],
        request_params=params,
    )


def get_research_run(run_id: str) -> Optional[ResearchRun]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM research_runs WHERE id = ?", (run_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row_to_research_run(row)
    return None


def get_latest_research_run() -> Optional[ResearchRun]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM research_runs ORDER BY started_at DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    if row:
        return row_to_research_run(row)
    return None


def get_preferences() -> UserPreferences:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT data FROM user_preferences WHERE id = 'default'")
    row = cursor.fetchone()
    conn.close()
    if row:
        try:
            data = json.loads(row["data"])
            return UserPreferences(**data)
        except Exception:
            pass
    return UserPreferences()


def save_preferences(prefs: UserPreferences) -> UserPreferences:
    conn = get_db_connection()
    cursor = conn.cursor()
    prefs.updated_at = datetime.now(timezone.utc).isoformat()
    cursor.execute(
        """
        INSERT OR REPLACE INTO user_preferences (id, data, updated_at)
        VALUES ('default', ?, ?)
        """,
        (prefs.model_dump_json(), prefs.updated_at),
    )
    conn.commit()
    conn.close()
    return prefs


def get_dashboard_stats() -> Dict[str, Any]:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM opportunities")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM opportunities WHERE status = 'new'")
    new_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM opportunities WHERE status = 'saved'")
    saved_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM opportunities WHERE status IN ('interested', 'applied', 'rejected')")
    tracked_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM opportunities WHERE status = 'applied'")
    applied_count = cursor.fetchone()[0]

    conn.close()
    latest_run = get_latest_research_run()

    return {
        "total_opportunities": total,
        "new_opportunities": new_count,
        "saved_opportunities": saved_count,
        "applications_tracked": tracked_count,
        "applied_count": applied_count,
        "last_research_run": latest_run.model_dump() if latest_run else None,
    }

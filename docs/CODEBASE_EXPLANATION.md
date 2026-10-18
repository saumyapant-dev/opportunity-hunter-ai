# Opportunity Hunter AI — Complete Codebase Explanation

This document provides a line-by-line and component-by-component architectural walkthrough of the entire **Opportunity Hunter AI** codebase.

---

## 1. Complete Project Directory Tree

```
opp-hunter/
│
├── backend/                              # Python FastAPI Backend & Agent Service
│   ├── app/
│   │   ├── __init__.py                   # Package initializer
│   │   ├── main.py                       # FastAPI application & CORS configuration
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── endpoints.py              # REST API routes & webhook receivers
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── opportunity.py            # Pydantic schemas (Opportunity, Run, Prefs)
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   └── db.py                     # SQLite connection, tables, indexes & CRUD
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── deduplication.py          # URL normalizer & duplicate detector
│   │   │   └── n8n_client.py             # n8n webhook dispatcher & health ping
│   │   └── agents/
│   │       ├── __init__.py
│   │       └── browser_researcher.py     # Browser Use agent & mock research engine
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_api.py                   # Automated API & deduplication tests
│   │   └── test_browser_agent.py         # Schema & mock generator tests
│   ├── data/
│   │   └── opportunities.db              # SQLite persistent database file
│   ├── requirements.txt                  # Python dependencies
│   ├── .env                              # Active environment variables (git-ignored)
│   └── .env.example                      # Template for environment variables
│
├── frontend/                             # React 18 + Vite + Tailwind Dashboard
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx                # Top navigation & system health badges
│   │   │   ├── Sidebar.jsx               # Navigation links & database stats widget
│   │   │   └── OpportunityCard.jsx       # Reusable card with inline status dropdown
│   │   ├── pages/
│   │   │   ├── DashboardPage.jsx         # KPI overview & recent discoveries
│   │   │   ├── DiscoverPage.jsx          # Search console & live execution stepper
│   │   │   ├── ResultsPage.jsx           # Filterable catalog with search bar
│   │   │   ├── SavedPage.jsx             # Application pipeline stage manager
│   │   │   └── SettingsPage.jsx          # User preferences & service diagnostics
│   │   ├── services/
│   │   │   └── api.js                    # Fetch HTTP client for backend REST API
│   │   ├── App.jsx                       # React Router container & global state
│   │   ├── main.jsx                      # DOM mount entrypoint
│   │   └── index.css                     # Tailwind directives & custom scrollbars
│   ├── public/                           # Static assets
│   ├── package.json                      # Node dependencies & build scripts
│   ├── vite.config.js                    # Vite dev server & backend API proxy
│   ├── tailwind.config.js                # Tailwind styling theme & color tokens
│   ├── postcss.config.js                 # PostCSS autoprefixer configuration
│   └── index.html                        # HTML root template with Plus Jakarta font
│
├── n8n/                                  # n8n Workflow Automation
│   ├── workflows/
│   │   ├── manual_opportunity_discovery.json   # On-demand webhook research pipeline
│   │   ├── scheduled_opportunity_discovery.json # Daily 8:00 AM cron harvester
│   │   └── email_notifications.json            # HTML email digest dispatcher
│   └── README.md                         # Workflow import & credential setup guide
│
├── docs/                                 # Complete Technical Documentation
│   ├── PROJECT_OVERVIEW.md
│   ├── ARCHITECTURE.md
│   ├── TECH_STACK.md
│   ├── DEVELOPMENT_GUIDE.md
│   ├── CODEBASE_EXPLANATION.md
│   ├── LEARNING_ROADMAP.md
│   ├── INTERVIEW_PREPARATION.md
│   ├── PROJECT_PITCH.md
│   ├── DEMO_SCRIPT.md
│   ├── TROUBLESHOOTING.md
│   └── Opportunity_Hunter_Complete_Study_Guide.pdf # Master PDF Study Guide
│
├── .browseruse/                          # Sandboxed Chromium user data profiles
├── .gitignore                            # Git exclusion rules
└── README.md                             # High-level project summary & quick start
```

---

## 2. Core Backend Files (Line-by-Line Breakdown)

### A. `backend/app/models/opportunity.py`
**Purpose**: Defines the data models that guarantee type safety across the entire backend.

```python
class OpportunityType(str, Enum):
    INTERNSHIP = "internship"
    HACKATHON = "hackathon"
    RESEARCH = "research"
    JOB = "job"
```
*Beginner Explanation*: An `Enum` (Enumeration) restricts string values to a strict set of choices. If a website extracts `"fellowship"`, our code maps it safely to `RESEARCH` instead of creating arbitrary new types.

```python
class Opportunity(OpportunityBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    discovered_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
```
*Beginner Explanation*: Generates a unique UUID string (e.g., `"db49933e-..."`) and an ISO-8601 UTC timestamp automatically whenever a new opportunity is created.

```python
class ExtractedOpportunity(BaseModel):
    title: str = Field(..., description="Specific opportunity or job/hackathon title")
    organization: str = Field(..., description="Organization, employer, or host name")
    type: str = Field(default="internship")
    description: str
    required_skills: List[str] = Field(default_factory=list)
    location: str = "Remote"
    remote: bool = True
    deadline: Optional[str] = Field(default=None, description="Actual deadline if found, else null. Never invent deadlines.")
    application_url: str
    source_url: str
    verification_status: str = "verified"

class OpportunityListOutput(BaseModel):
    opportunities: List[ExtractedOpportunity]
```
*Beginner Explanation*: This is the exact schema passed to Browser Use. The LLM receives the field descriptions as instructions: if a deadline is missing, it returns `null` rather than guessing a date.

---

### B. `backend/app/database/db.py`
**Purpose**: Direct SQLite interface for connection management, indexing, and CRUD queries.

```python
def init_db():
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
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_opp_normalized_url ON opportunities(normalized_url);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_opp_status ON opportunities(status);")
```
*Beginner Explanation*:
- Creates the `opportunities` table if it doesn't already exist.
- SQLite does not have a native `BOOLEAN` type, so `remote` is stored as an integer (`1` for true, `0` for false).
- `required_skills` is a JSON-serialized string (e.g. `'["Python", "React"]'`).
- `CREATE INDEX` builds B-tree lookup indexes on `normalized_url` and `status`, transforming search from a slow full-table scan ($O(N)$) into an instantaneous lookup ($O(\log N)$).

---

### C. `backend/app/services/deduplication.py`
**Purpose**: Normalizes URLs, identifies duplicate listings, and protects existing user application states.

```python
TRACKING_PARAMS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term",
    "utm_content", "ref", "source", "fbclid", "gclid", "trk"
}

def normalize_url(raw_url: str) -> str:
    parsed = urlparse(raw_url.strip())
    query_params = parse_qsl(parsed.query, keep_blank_values=False)
    filtered_params = [(k, v) for k, v in query_params if k.lower() not in TRACKING_PARAMS]
    filtered_params.sort(key=lambda x: x[0])
    query = urlencode(filtered_params)
    path = re.sub(r"/+", "/", parsed.path).rstrip("/")
    return urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), path, "", query, ""))
```
*Beginner Explanation*:
- `urlparse` breaks a URL into its parts: scheme (`https`), netloc (`devpost.com`), path (`/hackathons/ai-2026/`), and query (`?utm_source=twitter&ref=abc`).
- `filtered_params` strips out tracking keys like `utm_source` and `ref`.
- `path.rstrip("/")` removes trailing slashes so `site.com/job/` and `site.com/job` match identical database keys.

```python
if existing:
    duplicate_count += 1
    existing.discovered_at = datetime.now(timezone.utc).isoformat()
    # PRESERVE USER STATUS:
    save_opportunity(existing, normalized_url=norm_app_url)
    results.append(existing)
else:
    new_count += 1
    if not opp.status:
        opp.status = OpportunityStatus.NEW
    save_opportunity(opp, normalized_url=norm_app_url)
    results.append(opp)
```
*Beginner Explanation*: **The Status Preservation Guarantee**: If a job was previously marked by the student as `APPLIED`, finding it again updates the timestamp to show it's still active, but **never resets the status back to `NEW`**.

---

### D. `backend/app/agents/browser_researcher.py`
**Purpose**: Autonomous browser agent integration and mock fallback engine.

```python
# Set local config dir to prevent OS PermissionError
project_root = Path(__file__).resolve().parent.parent.parent.parent
default_config_dir = project_root / ".browseruse"
os.environ.setdefault("BROWSER_USE_CONFIG_DIR", str(default_config_dir))
```
*Beginner Explanation*: Prevents the common error where `browser-use` attempts to write into restricted system directories (`~/.config/browseruse`). Directs all profiles cleanly into the project's `.browseruse` folder.

```python
browser = Browser(headless=headless)
agent = Agent(
    task=prompt,
    llm=llm,
    browser=browser,
    output_model_schema=OpportunityListOutput,
    max_failures=3,
    step_timeout=120,
)
history = await agent.run(max_steps=20)
structured = history.get_structured_output(OpportunityListOutput)
```
*Beginner Explanation*:
- `Browser(headless=True)` launches Chromium without a visible window.
- `Agent(...)` connects the user prompt, the LLM, the browser instance, and the Pydantic output schema.
- `history.get_structured_output(...)` parses the final agent history directly into our typed Python schema.

---

### E. `backend/app/api/endpoints.py`
**Purpose**: Defines the REST endpoints and coordinates background workers.

```python
@router.post("/api/research", response_model=ResearchResponse, status_code=status.HTTP_202_ACCEPTED)
async def trigger_research(
    request: ResearchRequest,
    background_tasks: BackgroundTasks,
    use_n8n: Optional[bool] = Query(None),
):
    run_id = str(uuid.uuid4())
    run = ResearchRun(id=run_id, status=ResearchRunStatus.RUNNING, request_params=request.model_dump())
    create_research_run(run)

    # Route through n8n or direct background runner
    if should_use_n8n:
        n8n_result = await send_research_to_n8n(run_id=run_id, request=request)
        if n8n_result.get("success"):
            return ResearchResponse(run_id=run_id, status=ResearchRunStatus.RUNNING, orchestrator="n8n")

    background_tasks.add_task(_run_research_background, run_id, request)
    return ResearchResponse(run_id=run_id, status=ResearchRunStatus.RUNNING, orchestrator="direct")
```
*Beginner Explanation*:
- Returns `HTTP 202 Accepted` immediately so the client receives the `run_id` in milliseconds.
- `background_tasks.add_task(...)` queues the research execution in the background without blocking the HTTP server.

---

## 3. Core Frontend Files (Line-by-Line Breakdown)

### A. `frontend/src/services/api.js`
**Purpose**: Centralized HTTP client wrapping `fetch()`.

```python
export const api = {
  getOpportunities: (params = {}) => { ... },
  triggerResearch: (payload, useN8n = null) => { ... },
  getResearchRun: (runId) => request(`/api/research/${runId}`),
  updateOpportunity: (id, updates) => request(`/api/opportunities/${id}`, { method: 'PATCH', body: JSON.stringify(updates) }),
};
```
*Beginner Explanation*: Abstracting all `fetch` calls into a single service object means that if the backend URL ever changes, we only need to edit a single file instead of hunting through 10 different React components.

---

### B. `frontend/src/components/OpportunityCard.jsx`
**Purpose**: The reusable card component rendering an opportunity's metadata and interactive status controls.

```jsx
const handleStatusSelect = async (newStatus) => {
  setIsUpdating(true);
  setCurrentStatus(newStatus); // Optimistic UI update!
  try {
    if (onStatusChange) {
      await onStatusChange(opportunity.id, newStatus);
    }
  } catch (err) {
    setCurrentStatus(opportunity.status); // Rollback on error!
  } finally {
    setIsUpdating(false);
  }
};
```
*Beginner Explanation*: **Optimistic UI updating**: The dropdown updates the screen *immediately* when clicked. In the background, it sends the `PATCH` request. If the network fails, it catches the error and reverts back to the original status.

---

### C. `frontend/src/pages/DiscoverPage.jsx`
**Purpose**: The search console with live polling stepper.

```jsx
const pollInterval = setInterval(async () => {
  const runStatus = await api.getResearchRun(runId);
  if (runStatus.status === 'completed') {
    clearInterval(pollInterval);
    setExecutionStep(4);
    const results = await api.getOpportunities({ limit: maxResults });
    setNewlyDiscovered(results);
  }
}, 1200);
```
*Beginner Explanation*: Sets a non-blocking timer that checks the backend every 1.2 seconds. Once `runStatus.status === 'completed'`, it stops the timer and fetches the fresh results.

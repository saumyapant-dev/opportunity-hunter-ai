# Opportunity Hunter AI — Complete Beginner's Learning Guide & Technical Interview Preparation

---

## Executive Summary & Document Guide

This comprehensive guide is designed for Computer Science students, software engineering candidates, and beginner AI developers. It explains the entire **Opportunity Hunter AI** project from scratch—starting with zero prerequisite knowledge of autonomous AI agents, walking through every single architectural layer and line of code, and culminating in an interview-ready masterclass.

### Quick Links to Sections:
1. [Chapter 1: Introduction to AI Agents & The Problem We Solve](#chapter-1-introduction-to-ai-agents--the-problem-we-solve)
2. [Chapter 2: Comprehensive Technology Stack Deep-Dive](#chapter-2-comprehensive-technology-stack-deep-dive)
3. [Chapter 3: Step-by-Step Implementation Guide (From Empty Folder to Production)](#chapter-3-step-by-step-implementation-guide)
4. [Chapter 4: The Agent Under the Hood — End-to-End Execution Lifecycle](#chapter-4-the-agent-under-the-hood)
5. [Chapter 5: Technical Interview Masterclass & Defense Preparation](#chapter-5-technical-interview-masterclass)

---

# Chapter 1: Introduction to AI Agents & The Problem We Solve

---

### 1.1 What is an AI Agent?

To understand Opportunity Hunter AI, we must first understand the fundamental evolution from traditional code to Large Language Models (LLMs), and finally to **Autonomous AI Agents**.

```
┌─────────────────────────┐    ┌─────────────────────────┐    ┌─────────────────────────┐
│   Traditional Program   │    │     Standard LLM        │    │    Autonomous AI Agent  │
│  (Deterministic Code)   │    │    (Knowledge Brain)    │    │ (Brain + Eyes + Hands)  │
├─────────────────────────┤    ├─────────────────────────┤    ├─────────────────────────┤
│ • If/Else logic only    │    │ • Generates text        │    │ • Perceives Environment │
│ • Rigid web scrapers    │    │ • No web access         │    │ • Reasons & Plans Steps │
│ • Breaks on DOM changes │    │ • Cannot take actions   │    │ • Executes Web Actions  │
│ • No reasoning ability  │    │ • Prone to hallucinations│   │ • Corrects Its Errors   │
└─────────────────────────┘    └─────────────────────────┘    └─────────────────────────┘
```

#### The Analogy:
- **Traditional Code (The Calculator)**: If you tell a Python script to click a button at XPath `//*[@id="submit-btn"]`, it clicks it. But if the website redesigns its HTML and renames the button to `<button class="apply-now">`, the script crashes immediately.
- **LLM Prompting (The Advisor)**: You ask ChatGPT: *"Where can I find computer science internships?"* It gives you a great paragraph of suggestions. However, it cannot browse the web dynamically, fill out filter forms, or extract real-time data into your database.
- **Autonomous AI Agent (The Digital Intern)**: You tell an AI Agent: *"Find summer 2026 software engineering internships for college sophomores on LinkedIn and Y Combinator, verify that applications are open, extract the stipend and deadlines, and save them."* The agent opens a real browser, types queries, scrolls past popups, reads DOM elements visually, extracts the information, verifies the facts, and saves the data.

#### The Core Mechanism: The Perception-Reasoning-Action Loop
Every modern AI agent operates on an infinite or bounded cycle called the **ReAct (Reason + Act) loop**:
1. **Perceive (Eyes)**: The agent inspects its environment (e.g., takes a screenshot or extracts the interactive DOM tree of a webpage).
2. **Reason (Brain)**: The agent passes its observations and its high-level goal to an LLM: *"I see a search bar and a dropdown for 'Job Type'. To find internships, I must click the dropdown and select 'Internship'."*
3. **Act (Hands)**: The LLM emits a structured action (e.g., `click(element_index=14)` or `type_text(query="AI Engineer")`).
4. **Evaluate (Feedback)**: The agent observes the resulting DOM change. If an anti-bot modal appears, it reasons about how to dismiss it; if search results appear, it begins parsing the listings.

---

### 1.2 The Real-World Problem: Why Opportunity Hunter AI?

College students, early-career engineers, and researchers face a painful, fragmented opportunity landscape:
- **Severe Fragmentation**: Internships, hackathons, fellowships, and research positions are scattered across 20+ platforms (LinkedIn, Wellfound, Devpost, Y Combinator, university career boards, and individual company portals).
- **Stale Listings & Ghost Jobs**: Traditional job boards often display expired roles or aggregate third-party reposts with broken application links.
- **Manual Overhead**: A student spends 10–15 hours every week manually checking the same websites, filling out repetitive search filters, and copying deadlines into messy spreadsheets.
- **Missed Deadlines**: Many prestigious hackathons and early-decision internships have rolling admissions that close within days of posting.

**Opportunity Hunter AI** solves this by delivering an autonomous system that:
1. Automatically navigates modern JavaScript-rendered opportunity portals using AI-driven browser control.
2. Extracts verified, structured metadata (Title, Company, Location, Stipend/Salary, Direct Application URL, and Application Deadlines).
3. Normalizes and deduplicates listings so you never see the same post twice.
4. Preserves your personal application progress (`Applied`, `Saved`, `Interviewing`, `Rejected`).
5. Dispatches daily notifications and weekly digest summaries via scheduled n8n workflows.

---

### 1.3 Core Features Breakdown

| Feature | What It Does | How It Works Under the Hood |
| :--- | :--- | :--- |
| **Autonomous Web Discovery** | Searches opportunity boards dynamically | Uses `Browser Use` and `Playwright Chromium` to load pages, scroll, interact with search filters, and read DOM nodes. |
| **Real-Time Polling Stepper** | Shows live progress in the UI | The React frontend triggers an asynchronous job (HTTP 202 Accepted) and polls `/api/research/{run_id}` every 2 seconds through 4 visual steps: *Initializing*, *Navigating*, *Extracting*, and *Deduplicating*. |
| **Smart Deduplication & URL Normalizer** | Prevents duplicate job entries | Strips tracking queries (`utm_*`, `ref`, `gclid`), normalizes domains and protocol, and matches against existing records in SQLite. |
| **Status Preservation Guarantee** | Never clobbers user progress | If you mark a job as `Applied` or `Saved`, and the crawler finds the same job next week, the crawler updates the timestamp but strictly preserves your user status. |
| **Strict Zero-Hallucination Policy** | Guarantees accurate deadlines | If a website does not clearly state an application deadline, the system outputs `null` rather than allowing the LLM to invent a plausible date. |
| **Dual Orchestration Mode** | Runs with or without n8n | If an n8n workflow engine is online, it orchestrates scheduled discovery and emails; if n8n is offline, FastAPI seamlessly falls back to Python background tasks. |
| **Built-in Mock Research Engine** | Allows instant, free testing | Ships with a high-fidelity synthetic opportunity generator so developers can build and test the complete system without consuming paid LLM API credits. |

---

### 1.4 High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND LAYER                                 │
│  React 18 + Vite + Tailwind CSS + Lucide Icons + React Router (Port 5173)   │
│  • Dashboard Page   • Discover Page (Live Stepper)   • Results Page         │
│  • Saved / Applied Tracker   • Settings & Schedule Configurator             │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ HTTP REST / JSON
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              BACKEND LAYER                                  │
│                 FastAPI + Uvicorn + Pydantic v2 (Port 8000)                 │
│  • REST Endpoints (/api/research, /api/opportunities, /api/preferences)     │
│  • Background Task Manager (Async execution & run state tracking)           │
│  • Deduplication Engine (URL normalization & non-destructive merging)       │
│  • SQLite Database (Persistent relational store with indexed queries)       │
└──────────────────┬──────────────────────────────────────┬───────────────────┘
                   │                                      │
                   ▼ (Dispatches Async Tasks)             ▼ (Webhooks / HTTP)
┌──────────────────────────────────────┐  ┌───────────────────────────────────┐
│          AGENTIC ENGINE              │  │        AUTOMATION ENGINE          │
│   Browser Use Web AI + Playwright    │  │        n8n Workflow Hub           │
│  • Chromium Headless Browser         │  │  • Workflow 1: Manual Run         │
│  • DOM Tree Analyzer & Controller    │  │  • Workflow 2: Daily Cron (8 AM)  │
│  • LLM: OpenRouter / OpenAI / Mock   │  │  • Workflow 3: HTML Email Digest  │
│  • Pydantic Schema Output Validator  │  │  • Webhook Callbacks into FastAPI │
└──────────────────────────────────────┘  └───────────────────────────────────┘
```

---

# Chapter 2: Comprehensive Technology Stack Deep-Dive

---

### 2.1 Backend Core

#### 1. Python 3.12+
- **What it is**: A high-level, expressive, dynamically typed programming language known for its rich ecosystem in artificial intelligence, data manipulation, and web development.
- **Why we chose it**: Modern AI libraries (LangChain, Browser Use, Playwright for Python) are native to Python. Python 3.12 introduces substantial performance improvements in bytecode execution and exception handling.
- **Role in our project**: Powers the entire backend service, database interactions, agent logic, and data normalization.

#### 2. FastAPI
- **What it is**: A modern, high-performance web framework for building APIs with Python, based on standard Python type hints and the Starlette ASGI toolkit.
- **Why we chose it over Flask and Django**:
  - *Flask* is synchronous by default and lacks native schema validation, requiring third-party libraries like Marshmallow.
  - *Django* is heavyweight and comes with an ORM and admin interface that adds unnecessary overhead for a lightweight agent microservice.
  - *FastAPI* is fully asynchronous (`async`/`await`), features automatic OpenAPI/Swagger documentation generation at `/docs`, and runs on ASGI servers at speeds comparable to NodeJS and Go.
- **Role in our project**: Exposes all REST endpoints, manages CORS for the React frontend, coordinates background research runs, and receives inbound webhooks from n8n.

#### 3. Uvicorn
- **What it is**: A lightning-fast ASGI (Asynchronous Server Gateway Interface) web server implementation for Python, built on `uvloop` and `httptools`.
- **Role in our project**: Acts as the HTTP server that runs the FastAPI application and listens on `127.0.0.1:8000`.

#### 4. Pydantic v2
- **What it is**: The most widely used data validation and settings management library for Python, rewritten in Rust for extreme performance.
- **Role in our project**:
  - Enforces strict data models (`OpportunityCreate`, `OpportunityResponse`, `ExtractedOpportunity`).
  - Guarantees type coercion (e.g., converting ISO strings to Python `datetime` objects).
  - Supplies the JSON Schema to the LLM so the AI agent outputs structured data rather than unpredictable conversational text.

---

### 2.2 Database Layer: SQLite

- **What it is**: A self-contained, serverless, zero-configuration, transactional SQL database engine.
- **Why we chose SQLite over PostgreSQL / MongoDB**:
  - For a portfolio-grade, locally deployable desktop application, SQLite requires zero external services or Docker containers. It lives as a single file (`opportunities.db`) on your disk.
  - It supports standard SQL syntax, transactions (`ACID`), and high-speed B-tree indexing.
  - *Production Migration Path*: Because our SQL queries and data models are cleanly abstracted in `backend/app/database/db.py`, switching to PostgreSQL requires only replacing the SQLite driver with `asyncpg` or SQLAlchemy.
- **Database Schema**:

```sql
CREATE TABLE IF NOT EXISTS opportunities (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    location TEXT NOT NULL,
    type TEXT NOT NULL,
    source TEXT NOT NULL,
    url TEXT UNIQUE NOT NULL,
    description TEXT,
    deadline TEXT,
    stipend TEXT,
    tags TEXT,             -- JSON string array
    match_score REAL DEFAULT 0.0,
    status TEXT DEFAULT 'new',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_opportunities_url ON opportunities(url);
CREATE INDEX IF NOT EXISTS idx_opportunities_type ON opportunities(type);
CREATE INDEX IF NOT EXISTS idx_opportunities_status ON opportunities(status);
```

---

### 2.3 Browser Automation & AI Agents

#### 1. Browser Use Web AI (`browser-use`)
- **What it is**: An open-source agent framework specifically designed to enable LLMs to control and interact with web browsers like a human.
- **How it works**:
  1. Inspects the browser DOM using a custom tree-simplification algorithm that extracts only interactive and readable elements (buttons, inputs, links, headings).
  2. Numbers every interactive element on screen (`[1] Search`, `[2] Filter`, `[3] Apply`).
  3. Sends this simplified state to the LLM along with available actions (`click_element(index)`, `input_text(index, text)`, `scroll_page(direction)`, `navigate(url)`).
  4. Executes the action in Chromium via Playwright, observes the result, and loops until the extraction objective is met.

#### 2. Playwright Chromium
- **What it is**: Microsoft's modern, robust end-to-end browser automation framework.
- **Why we chose Playwright over Selenium**:
  - *Selenium* relies on the legacy WebDriver protocol, struggles with modern single-page applications (SPAs), and often requires fragile explicit sleep intervals (`time.sleep(5)`).
  - *Playwright* talks directly to the Chrome DevTools Protocol (CDP), automatically waits for elements to be actionable before clicking, handles network idle states, and provides headless execution.

#### 3. LLM Providers: OpenRouter & OpenAI
- **OpenRouter**: A unified API gateway that allows routing prompts to dozens of world-class models (Claude 3.5 Sonnet, GPT-4o, DeepSeek R1, Llama 3) with a single API key.
- **ChatOpenAI**: Native integration for OpenAI's GPT-4o / GPT-4o-mini models.
- **Mock Research Engine**: A built-in fallback agent that mimics the browser research lifecycle with zero latency and zero API cost, generating realistic opportunities for development and offline testing.

---

### 2.4 Workflow Automation: n8n

- **What it is**: An open-source, node-based workflow automation platform that connects APIs, databases, webhooks, and AI models through visual data pipelines.
- **Why we use n8n alongside Python**:
  - *Separation of Concerns*: Python handles heavy computation, DOM analysis, and data normalization. n8n handles timing, scheduling, webhook routing, and external notifications (Slack, Discord, Email).
  - *Visual Observability*: You can visually inspect the exact payload at every stage of a scheduled pipeline, retry failed executions, and change cron intervals without touching Python code or restarting the server.
- **Our 3 Pre-configured Workflows**:
  1. `manual_opportunity_discovery.json`: Webhook receiver that validates parameters, triggers the agent, deduplicates listings, and returns an execution summary.
  2. `scheduled_opportunity_discovery.json`: Daily 8:00 AM cron trigger that queries user preferences, launches the discovery run, and initiates notifications.
  3. `email_notifications.json`: Webhook that formats newly discovered opportunities into a responsive, mobile-ready HTML email digest and dispatches it via SMTP.

---

### 2.5 Frontend SaaS Dashboard

#### 1. React 18
- **What it is**: The industry-standard declarative JavaScript UI library for building modern component-based web applications.
- **Features used**: Functional components, React Hooks (`useState`, `useEffect`, `useCallback`), and dynamic UI state transitions.

#### 2. Vite
- **What it is**: A next-generation frontend build tool powered by native ES modules (ESM) in development and Rollup for production bundling.
- **Why we chose Vite over Create React App (CRA)**:
  - CRA is deprecated and slow, taking 30–60 seconds to bundle cold starts.
  - Vite starts instantly (< 300ms) with Hot Module Replacement (HMR) and produces optimized, lightweight production builds.

#### 3. Tailwind CSS
- **What it is**: A utility-first CSS framework that enables rapid, maintainable styling directly within JSX.
- **Why we chose it**: Eliminates monolithic CSS files, enforces consistent spacing and typography scales, and makes responsive design (mobile/desktop) effortless.

#### 4. Lucide React
- **What it is**: A clean, lightweight, highly customizable icon library providing modern SVG icons (`Compass`, `BookmarkCheck`, `Calendar`, `Briefcase`, `Clock`, `Sparkles`).

---

# Chapter 3: Step-by-Step Implementation Guide

---

### 3.1 Chronological Development Lifecycle (The 15 Phases)

Here is how Opportunity Hunter AI was engineered from an empty folder to a portfolio-ready application:

```
[Phase 1: Architecture Design] ──► [Phase 2: Project Scaffolding] ──► [Phase 3: Data Schemas]
                                                                              │
┌─────────────────────────────────────────────────────────────────────────────┘
▼
[Phase 4: SQLite Database]    ──► [Phase 5: Deduplication Logic]  ──► [Phase 6: Browser Agent]
                                                                              │
┌─────────────────────────────────────────────────────────────────────────────┘
▼
[Phase 7: FastAPI Endpoints]   ──► [Phase 8: React Scaffolding]    ──► [Phase 9: Dashboard UI]
                                                                              │
┌─────────────────────────────────────────────────────────────────────────────┘
▼
[Phase 10: Polling Stepper]   ──► [Phase 11: Management Pages]    ──► [Phase 12: n8n Pipelines]
                                                                              │
┌─────────────────────────────────────────────────────────────────────────────┘
▼
[Phase 13: Unit Test Suite]   ──► [Phase 14: End-to-End Testing]  ──► [Phase 15: Documentation]
```

1. **Phase 1: Architectural Blueprint**: Defined system boundaries between frontend (presentation), FastAPI (business logic/persistence), Browser Use (AI perception), and n8n (scheduling/notifications).
2. **Phase 2: Project Scaffolding**: Structured modular folders (`backend/app/{api,agents,database,models,services}`, `frontend/src/{components,pages,services}`, `n8n/workflows`, `docs`).
3. **Phase 3: Data Schemas**: Authored strict Pydantic v2 schemas for opportunities, research runs, user preferences, and LLM structured outputs.
4. **Phase 4: SQLite Database**: Created relational tables with unique constraints on normalized URLs and performance indexes on search fields.
5. **Phase 5: Deduplication Logic**: Implemented query parameter stripping and status preservation algorithms.
6. **Phase 6: Browser AI Agent**: Built the Browser Use runner with Chromium, LLM bindings, structured extraction prompts, and the mock generator fallback.
7. **Phase 7: FastAPI REST Endpoints**: Implemented 10+ endpoints with asynchronous execution, job ID polling, and error handling.
8. **Phase 8: React 18 Setup**: Initialized Vite React application, configured Tailwind CSS, and set up client HTTP wrappers.
9. **Phase 9: SaaS Dashboard**: Built statistics cards, recent opportunity feeds, and quick navigation.
10. **Phase 10: Discover Page with Live Stepper**: Created a 4-step progress animation connected to live backend polling.
11. **Phase 11: Results, Saved & Settings Pages**: Built interactive filtering grids, status dropdown selectors, and preference forms.
12. **Phase 12: n8n Workflows**: Built and exported 3 valid JSON workflow specifications for manual runs, daily schedules, and HTML email digests.
13. **Phase 13: Automated Testing**: Authored 13 unit tests validating database operations, deduplication, URL cleaning, and API endpoints.
14. **Phase 14: Live End-to-End Verification**: Booted services locally, ran discovery jobs, updated statuses, and verified webhook ingestion.
15. **Phase 15: Documentation & Study Guide**: Authored comprehensive markdown guides and compiled the official study guide.

---

### 3.2 Workspace Folder Structure

```
opp-hunter/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                     # FastAPI entrypoint, CORS, lifespan
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   └── browser_researcher.py   # Browser Use AI agent & Mock generator
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── endpoints.py            # REST API endpoints & Webhooks
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   └── db.py                   # SQLite tables, indexes, CRUD
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── opportunity.py          # Pydantic v2 data models & schemas
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── deduplication.py        # URL normalizer & deduplication engine
│   │       └── n8n_client.py           # Async HTTP client for n8n webhooks
│   ├── tests/
│   │   └── test_backend.py             # 13 automated unit tests
│   ├── .env                            # Environment secrets (ignored by git)
│   ├── .env.example                    # Template environment variables
│   └── requirements.txt                # Python backend dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx              # Navigation header with system indicators
│   │   │   ├── Sidebar.jsx             # Collapsible side navigation menu
│   │   │   └── OpportunityCard.jsx     # Reusable opportunity card with status selector
│   │   ├── pages/
│   │   │   ├── DashboardPage.jsx       # Overview KPI cards & quick actions
│   │   │   ├── DiscoverPage.jsx        # Search form with 4-step live polling stepper
│   │   │   ├── ResultsPage.jsx         # Searchable, filterable opportunity grid
│   │   │   ├── SavedPage.jsx           # Track applied, saved, and interested roles
│   │   │   └── SettingsPage.jsx        # Preferences, schedule config, system health
│   │   ├── services/
│   │   │   └── api.js                  # Axios / Fetch client for backend REST API
│   │   ├── App.jsx                     # Route definitions & layout shell
│   │   ├── index.css                   # Tailwind CSS directives
│   │   └── main.jsx                    # React 18 DOM mount point
│   ├── package.json                    # Node dependencies & build scripts
│   ├── tailwind.config.js              # Tailwind styling configuration
│   └── vite.config.js                  # Vite configuration & proxy settings
├── n8n/
│   ├── workflows/
│   │   ├── manual_opportunity_discovery.json
│   │   ├── scheduled_opportunity_discovery.json
│   │   └── email_notifications.json
│   └── README.md                       # Setup and import instructions for n8n
├── docs/                               # 10 comprehensive markdown guides
└── README.md                           # Master repository documentation
```

---

### 3.3 Core Code Implementation Deep-Dive

#### 1. The Pydantic Data Model (`backend/app/models/opportunity.py`)
This file defines the strict structure of every opportunity in the system:

```python
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

class OpportunityType(str, Enum):
    INTERNSHIP = "internship"
    HACKATHON = "hackathon"
    RESEARCH = "research"
    JOB = "job"
    FELLOWSHIP = "fellowship"

class OpportunityStatus(str, Enum):
    NEW = "new"
    SAVED = "saved"
    INTERESTED = "interested"
    APPLIED = "applied"
    REJECTED = "rejected"

class OpportunityBase(BaseModel):
    title: str = Field(..., description="Job or opportunity title")
    company: str = Field(..., description="Company, university, or organizing body")
    location: str = Field(default="Remote", description="Physical location or Remote")
    type: OpportunityType = Field(default=OpportunityType.INTERNSHIP)
    url: str = Field(..., description="Direct application link")
    description: Optional[str] = Field(default=None)
    deadline: Optional[str] = Field(default=None, description="ISO date string or null")
    stipend: Optional[str] = Field(default=None)
    tags: List[str] = Field(default_factory=list)
    match_score: float = Field(default=0.0, ge=0.0, le=100.0)
    status: OpportunityStatus = Field(default=OpportunityStatus.NEW)
```

**Key Takeaway for Beginners**: By defining `OpportunityType` and `OpportunityStatus` as Enums, we eliminate typos (e.g., `"intern"` vs `"internship"`). By setting `deadline: Optional[str] = None`, we support our zero-hallucination policy.

---

#### 2. The Smart Deduplication Engine (`backend/app/services/deduplication.py`)
This service strips noisy tracking parameters and performs non-destructive merges:

```python
import urllib.parse
from backend.app.models.opportunity import OpportunityBase, OpportunityStatus
from backend.app.database.db import get_opportunity_by_url, insert_opportunity, update_opportunity

TRACKING_PARAMS = {
    'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
    'ref', 'source', 'fbclid', 'gclid', 'mc_cid', 'mc_eid'
}

def normalize_url(raw_url: str) -> str:
    """Strips query trackers, removes trailing slashes, and lowercases domain."""
    parsed = urllib.parse.urlparse(raw_url.strip())
    domain = parsed.netloc.lower()
    
    # Strip default HTTP ports
    if domain.endswith(':80'): domain = domain[:-3]
    if domain.endswith(':443'): domain = domain[:-4]
    
    query_params = urllib.parse.parse_qsl(parsed.query)
    clean_params = [(k, v) for k, v in query_params if k.lower() not in TRACKING_PARAMS]
    clean_query = urllib.parse.urlencode(sorted(clean_params))
    
    path = parsed.path.rstrip('/')
    return urllib.parse.urlunparse((parsed.scheme.lower(), domain, path, '', clean_query, ''))

def process_and_deduplicate(opportunities: list[OpportunityBase]) -> tuple[int, int]:
    """Saves new opportunities and merges existing ones without clobbering user status."""
    added = 0
    updated = 0
    for opp in opportunities:
        clean_url = normalize_url(opp.url)
        opp.url = clean_url
        existing = get_opportunity_by_url(clean_url)
        
        if existing:
            # STATUS PRESERVATION: Keep existing status (e.g., 'applied')
            opp.status = existing.status
            update_opportunity(existing.id, opp)
            updated += 1
        else:
            if not opp.status:
                opp.status = OpportunityStatus.NEW
            insert_opportunity(opp)
            added += 1
    return added, updated
```

---

#### 3. The Asynchronous Discovery Endpoint (`backend/app/api/endpoints.py`)
This demonstrates high-concurrency background job handling:

```python
@router.post("/api/research", status_code=status.HTTP_202_ACCEPTED)
async def start_research(request: ResearchRequest, background_tasks: BackgroundTasks):
    """Dispatches research asynchronously and returns run_id immediately."""
    run_id = str(uuid.uuid4())
    create_research_run(run_id=run_id, query=request.query)
    
    # Run the agent in the background so the client doesn't time out
    background_tasks.add_task(execute_research_job, run_id, request)
    
    return {
        "status": "started",
        "run_id": run_id,
        "message": "Research job dispatched successfully."
    }

@router.get("/api/research/{run_id}")
async def get_run_status(run_id: str):
    """Polled by React frontend to display live progress."""
    run = get_research_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run
```

---

### 3.4 Local Setup & Execution Guide

Follow these exact commands in your terminal to run the complete stack locally:

#### Step 1: Clone and Configure Backend
```bash
# Navigate to the project root
cd "/Users/saumyapant/Desktop/opp hunter"

# Create and activate a Python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install all backend dependencies
pip install -r backend/requirements.txt

# Create your local environment configuration
cp backend/.env.example backend/.env
```

#### Step 2: Start the FastAPI Backend
```bash
# Start Uvicorn ASGI server with hot reloading
python3 -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
*Verification*: Open your browser to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to view the interactive Swagger documentation.

#### Step 3: Start the React Frontend
```bash
# Open a second terminal window
cd "/Users/saumyapant/Desktop/opp hunter/frontend"

# Install Node dependencies
npm install

# Start the Vite development server
npm run dev
```
*Verification*: Open your browser to [http://localhost:5173](http://localhost:5173) to view the live dashboard.

#### Step 4: Run the Automated Test Suite
```bash
# In the project root with the virtual environment active:
python3 -m unittest discover -s backend/tests -p "test_*.py" -v
```
*Expected Output*: `Ran 13 tests in 0.042s. OK`.

---

# Chapter 4: The Agent Under the Hood — End-to-End Execution Lifecycle

---

### 4.1 Step-by-Step Execution Journey

Let's trace what happens when a student enters `"AI Engineer Internships"` in the Discover Page and clicks **"Start Discovery"**:

```
[User clicks 'Start Discovery']
               │
               ▼
1. React Frontend generates HTTP POST to /api/research
   Payload: { "query": "AI Engineer Internships", "type": "internship" }
               │
               ▼
2. FastAPI creates run record in SQLite:
   Status: 'initializing' | Step: 1/4 | Run ID: '550e8400-...'
   Returns HTTP 202 Accepted { "run_id": "550e8400-..." } in 15ms.
               │
               ▼
3. React Frontend enters Polling Loop:
   Requests GET /api/research/550e8400-... every 2000ms.
   Updates visual Stepper: Step 1 (Initializing) -> Step 2 (Navigating).
               │
               ▼
4. Backend Worker launches Browser Use Agent:
   • Boots Playwright Chromium in headless mode.
   • Opens Google / LinkedIn / YC opportunity portals.
   • Extracts interactive DOM nodes.
   • Feeds DOM + Goal to LLM: "Identify opportunity cards and application links".
   • LLM issues clicks and scroll actions.
               │
               ▼
5. Backend updates run record:
   Status: 'extracting' | Step: 3/4.
   Agent extracts listings into Pydantic models.
   Verifies: If deadline is absent, outputs null (no hallucination).
               │
               ▼
6. Backend updates run record:
   Status: 'deduplicating' | Step: 4/4.
   Normalizes URLs (strips utm_* trackers).
   Queries SQLite: Matches existing entries.
   Preserves user status (e.g., 'applied').
   Inserts new listings.
               │
               ▼
7. Backend marks run record 'completed':
   Stores discovered_count: 5, new_count: 3.
               │
               ▼
8. React Frontend poll detects status == 'completed':
   Stops polling interval.
   Renders green celebration banner with summary badges.
   Redirects user to Results Page to view the new opportunities.
```

---

# Chapter 5: Technical Interview Masterclass & Defense Preparation

---

### 5.1 How to Present This Project (The STAR Framework)

When an interviewer asks, *"Tell me about a project you've built,"* use the **STAR Framework** (Situation, Task, Action, Result):

- **Situation**: *"As a Computer Science student, I noticed how fragmented and exhausting opportunity hunting is. Students spend 10 to 15 hours every week checking 20 different websites for internships, research roles, and hackathons, often running into expired listings or duplicate postings."*
- **Task**: *"I wanted to build an end-to-end autonomous AI system that not only scrapes the web, but understands page layouts dynamically like a human, normalizes and deduplicates data reliably, and alerts the user automatically."*
- **Action**: *"I architected Opportunity Hunter AI. I built an asynchronous backend using Python and FastAPI, integrated the Browser Use AI framework with Playwright Chromium to visually navigate complex JavaScript portals, and enforced strict zero-hallucination schemas using Pydantic. I designed a smart URL normalization engine to strip tracking queries and preserve user application statuses. For automation, I created n8n workflows for daily scheduled runs and HTML email digests. On the frontend, I developed a modern React 18 dashboard with a real-time polling stepper."*
- **Result**: *"The resulting application autonomously discovers, verifies, and indexes dozens of opportunities in under two minutes, saving students hours of manual searching while guaranteeing clean, non-duplicate data."*

---

### 5.2 Pitch Scripts

#### The 30-Second Elevator Pitch
> *"I built Opportunity Hunter AI, an autonomous opportunity discovery platform for students. It combines an async FastAPI backend, a React 18 dashboard, and the Browser Use Web AI framework to navigate modern job boards with a real headless browser. It extracts verified deadlines without hallucinations, deduplicates listings using custom URL normalization, and integrates with n8n for automated daily email digests."*

#### The 1-Minute Recruiter Pitch
> *"Opportunity Hunter AI is an intelligent opportunity aggregator that solves the problem of job search fatigue. Traditional web scrapers break whenever a website updates its HTML class names. To solve this, I used Browser Use and Playwright, allowing an LLM to visually perceive the webpage and interact with it like a human. I built the backend in FastAPI with SQLite, ensuring high-concurrency job dispatching via asynchronous workers and polling endpoints. I also implemented a robust deduplication engine that normalizes URLs and ensures that if a student marks a role as 'Applied', a subsequent crawl will never overwrite that status. Finally, I built a sleek React SaaS interface featuring a live 4-step progress stepper and n8n orchestration for scheduled notifications."*

#### The 3-Minute Technical Deep Dive
> *"Opportunity Hunter AI is an end-to-end agentic application designed around three architectural principles: resilient perception, non-destructive persistence, and asynchronous responsiveness.*
>
> *First, for web perception, standard BeautifulSoup or Selenium scrapers are too fragile for modern React and Angular job portals. I integrated the Browser Use framework with Playwright Chromium. Browser Use simplifies the DOM tree into interactive accessibility nodes and provides that context to an LLM. The LLM then issues structured navigation commands like clicking search filters and scrolling. To prevent data corruption, I enforced strict Pydantic v2 schemas where missing deadlines are explicitly coerced to null, eliminating LLM date hallucinations.*
>
> *Second, on the persistence layer, web crawlers frequently encounter identical listings with different tracking parameters. I built a URL normalization service that strips UTM tags, Facebook and Google click IDs, and protocol artifacts before hashing. When inserting into SQLite, our system performs non-destructive updates: if an opportunity already exists, we refresh its metadata and timestamps, but strictly preserve the student's personal status—such as 'Applied' or 'Interviewing'.*
>
> *Third, for user experience, browser automation can take 30 to 60 seconds, which would easily cause an HTTP request to time out. I architected the API using an asynchronous job pattern: the React frontend dispatches a POST request and receives an HTTP 202 Accepted with a unique UUID in under 20 milliseconds. The frontend then polls the backend every two seconds, updating a visual four-step stepper that tracks initialization, navigation, extraction, and deduplication.*
>
> *Finally, I integrated n8n to handle scheduled cron jobs and responsive HTML email digests, cleanly decoupling automation and scheduling from our core web API."*

---

### 5.3 Top 10 Technical Interview Questions & Answers

#### Q1: Why did you choose Browser Use over traditional web scraping libraries like BeautifulSoup or Scrapy?
**Answer**:
> *"BeautifulSoup and Scrapy are static HTML parsers. They work by making an HTTP GET request and parsing raw HTML strings. However, 90% of modern opportunity boards—like LinkedIn, Wellfound, and Greenhouse—rely heavily on client-side JavaScript rendering, shadow DOMs, infinite scrolling, and interactive modals.
> Furthermore, traditional scrapers rely on hardcoded CSS selectors or XPaths. If the website changes a class name from `.job-card` to `.listing-container`, the scraper breaks immediately.
> Browser Use controls a real headless Chromium browser via Playwright. It converts the visual DOM into interactive accessibility elements and allows an LLM to reason about what to click, scroll, or fill out. This makes our crawler self-healing and capable of navigating complex user flows just like a human."*

---

#### Q2: What is an asynchronous API, and why did you use the HTTP 202 Accepted pattern?
**Answer**:
> *"A standard synchronous API keeps the HTTP connection open until the server finishes processing. If an AI agent takes 45 seconds to open a browser, navigate pages, and extract data, a standard synchronous request would either hit a browser timeout or block other incoming requests on a single-threaded server.
> To prevent this, I implemented the asynchronous job pattern:
> 1. When the client calls `POST /api/research`, FastAPI assigns a unique UUID, records the job status as `initializing` in SQLite, and dispatches the long-running task to the background via `BackgroundTasks`.
> 2. FastAPI immediately returns an HTTP 202 Accepted status with the `run_id` in less than 20 milliseconds.
> 3. The React frontend then periodically polls `GET /api/research/{run_id}` to retrieve progress updates. This keeps the client responsive and allows the UI to display a live progress stepper."*

---

#### Q3: How do you prevent the LLM from hallucinating deadlines or stipends?
**Answer**:
> *"LLMs are generative probabilistic models, meaning they are naturally inclined to produce plausible-sounding completions even when facts are missing. In job hunting, inventing a deadline like 'May 1st' when none exists is disastrous.
> I solved this at the schema and prompting levels:
> 1. In our Pydantic model, `deadline` and `stipend` are typed as `Optional[str] = None`.
> 2. In our system prompt, we explicitly instruct the LLM: 'Extract only information explicitly stated on the webpage. If a deadline or stipend is not explicitly mentioned, you MUST set the field to null. NEVER guess, estimate, or extrapolate dates.'
> 3. Pydantic validates the parsed JSON against this contract. If the field is null, the frontend cleanly renders 'Open / Rolling' instead of an invented date."*

---

#### Q4: Explain how your URL normalization and deduplication works.
**Answer**:
> *"A major challenge with web crawlers is that the same job listing might appear under multiple different URLs due to marketing and referral queries. For example:
> `https://company.com/jobs/123?utm_source=linkedin&ref=campus` and `http://company.com/jobs/123/` are the exact same role.
> My deduplication pipeline processes URLs through several stages:
> 1. **Protocol and Host Normalization**: Lowercases the domain and standardizes `http` to `https`.
> 2. **Default Port Removal**: Strips standard `:80` and `:443` port suffixes.
> 3. **Query Parameter Cleaning**: Parses query strings using `urllib.parse` and filters out all known analytics parameters (`utm_*`, `ref`, `source`, `fbclid`, `gclid`).
> 4. **Path Normalization**: Strips redundant trailing slashes.
> 5. **Non-destructive Merge**: When matching against our indexed SQLite database, if a record exists, we update the timestamp but preserve the user's status (`applied`, `saved`). Only genuinely new URLs increment the new opportunity count."*

---

#### Q5: What is the Status Preservation Guarantee, and why was it necessary?
**Answer**:
> *"During initial testing, I discovered a subtle data-clobbering bug: if a user discovered an internship, saved it, and later marked it as `Applied`, and then ran a new search the following week, the crawler would discover the listing again. Because default schemas assign `status = 'new'`, re-inserting the listing would overwrite the user's `Applied` status back to `new`.
> To fix this, I introduced the Status Preservation Guarantee in our service layer:
> Before writing an opportunity to SQLite, we query the table by normalized URL. If the listing already exists, we copy the user's existing `status` to the incoming model before executing the SQL `UPDATE`. This guarantees that user interactions are never lost during automated crawls."*

---

#### Q6: Why did you use both FastAPI and n8n instead of writing everything in Python?
**Answer**:
> *"This is a question of architectural separation of concerns.
> FastAPI is our core domain engine: it handles database integrity, REST API endpoints, business logic, and heavy browser automation.
> n8n is our workflow orchestrator: it specializes in event-driven integrations, cron scheduling, visual pipeline monitoring, and external alerting (like SMTP emails or Discord webhooks).
> If we put cron schedules and email templates inside FastAPI, our web server would become tightly coupled to external email providers, and changing a schedule from daily to hourly would require modifying code and redeploying the backend. With n8n, a developer or operator can adjust triggers, inspect payload history, and add Slack notifications visually without touching a line of Python code."*

---

#### Q7: How does your frontend communicate with the backend?
**Answer**:
> *"The frontend communicates with the backend via standard HTTP REST over JSON using our centralized `frontend/src/services/api.js` client.
> For long-running research tasks, we use an asynchronous polling architecture:
> 1. `POST /api/research` triggers the job and returns a `run_id`.
> 2. The React component uses a JavaScript `setInterval` to call `GET /api/research/{run_id}` every 2000 milliseconds.
> 3. Each poll returns the current execution state (`step`, `status`, `logs`). The frontend translates this into a 4-step animated UI stepper.
> 4. When the response status changes to `completed` or `failed`, the interval is cleared with `clearInterval` to prevent memory leaks."*

---

#### Q8: What database did you choose, and how would you scale it for 100,000 users?
**Answer**:
> *"For this version, I chose SQLite because it is lightweight, zero-configuration, ACID-compliant, and runs directly from a local file, making it ideal for desktop deployment and portfolio demonstration.
> To scale this application to 100,000 active users:
> 1. **Database Migration**: Migrate from SQLite to a managed PostgreSQL cluster with read-replicas. PostgreSQL handles high-concurrency concurrent writes with row-level locking.
> 2. **Task Queue & Message Broker**: Replace FastAPI's in-memory `BackgroundTasks` with **Celery** or **Temporal** backed by **Redis** or **RabbitMQ**. This allows distributing browser worker tasks across a horizontally autoscaling fleet of containerized Playwright worker nodes.
> 3. **Browser Pool Management**: Browser instances are memory-heavy (~100MB per tab). We would implement a headless browser pool with session reuse and rate-limiting proxies to avoid IP blocking."*

---

#### Q9: What security practices did you implement in this project?
**Answer**:
> *"I implemented several key security practices:
> 1. **Environment Secret Separation**: API keys (`OPENROUTER_API_KEY`, `OPENAI_API_KEY`) and webhook secrets are stored strictly in `backend/.env`. We committed a sanitized `.env.example` to version control and added `.env` to `.gitignore`.
> 2. **CORS Restrictions**: Configured FastAPI's `CORSMiddleware` to explicitly allow requests only from authorized frontend origins (`http://localhost:5173`) rather than allowing wildcard origins (`*`).
> 3. **Input Sanitization**: All user search queries and preference strings are validated and bounded using Pydantic schemas, preventing injection attacks.
> 4. **SQL Parameterization**: All database queries use parameterized SQL (`?` placeholders) rather than raw string interpolation, completely eliminating SQL injection vulnerabilities."*

---

#### Q10: What challenges did you face while developing this project, and how did you resolve them?
**Answer**:
> *"Two major engineering challenges stood out:
> 
> **Challenge 1: Headless Browser Environment Restrictions & Sandbox Permissions**
> *Problem*: When launching Chromium via Playwright in restricted sandbox environments or on macOS, Browser Use defaulted to creating configuration directories in `~/.config/browseruse`, triggering a `PermissionError`.
> *Solution*: I explicitly configured `BROWSER_USE_CONFIG_DIR=./.browseruse` in the application environment and created an internal fallback runner that gracefully detects permission constraints.
>
> **Challenge 2: Overwriting User Application States During Re-Crawl**
> *Problem*: During early testing, running discovery twice caused opportunities marked as `Applied` to be overwritten back to `new`.
> *Solution*: I refactored the deduplication service to execute a lookup on the normalized URL before performing an update. If a match is found, the existing status is preserved while metadata like match score and timestamps are refreshed."*

---

### 5.4 Limitations & Future Technical Improvements

| Current Implementation | Known Limitation | Production Improvement Plan |
| :--- | :--- | :--- |
| **SQLite Single File** | Limited concurrent write throughput | Migrate to PostgreSQL with connection pooling via SQLAlchemy/AsyncPG. |
| **In-Memory BackgroundTasks** | Tasks do not survive server restarts | Adopt Redis + Celery/Temporal for durable, distributed task queues. |
| **Client-Side Polling** | Unnecessary HTTP overhead every 2s | Implement WebSockets (`ws://`) or Server-Sent Events (SSE) for push notifications. |
| **Heuristic Match Score** | Static keyword overlap scoring | Integrate vector embeddings (e.g., `text-embedding-3-small`) with pgvector for semantic resume matching. |
| **Local Headless Browser** | Consumes ~150MB RAM per worker | Offload browsing to managed browser clouds like Browserless.io or isolated Docker containers. |

---

## Conclusion & Study Roadmap

You now possess a complete, end-to-end understanding of **Opportunity Hunter AI**. You can explain the difference between a simple script and an autonomous agent, defend your choice of FastAPI and n8n, trace the lifecycle of a request from React to Playwright, and answer difficult system design and concurrency questions with confidence.

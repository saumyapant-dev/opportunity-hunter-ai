# Opportunity Hunter AI — Complete Development Guide (15 Phases from Scratch)

This guide takes you step-by-step through the entire chronological engineering journey of how **Opportunity Hunter AI** was designed, architected, coded, tested, and prepared for deployment.

---

## Phase 1: Problem Identification & Definition

### 1. What We Are Building
An autonomous opportunity discovery engine for students.

### 2. Why We Need It
Students spend hours searching across fragmented portals (Devpost, Hacker News, YC jobs, university sites) and repeatedly encounter expired deadlines, irrelevant senior roles, and duplicate cross-postings.

### 3. What Happens Internally
We establish concrete product requirements:
- Input: User technical skills, category preference, location, and experience.
- Process: Autonomous browser navigation, dynamic DOM parsing, entity extraction, URL normalization, and deduplication.
- Output: Typed, persistent records with direct application links, tracked through an interactive dashboard.

### 4. Files & Technologies
- Concept documentation (`docs/PROJECT_OVERVIEW.md`).

### 5. Verification
Interview test: Can you articulate the problem in 2 sentences? *"Students waste 10 hours a week checking disconnected job sites. Opportunity Hunter AI deploys an autonomous browser agent that discovers, filters, deduplicates, and tracks relevant student opportunities in one place."*

---

## Phase 2: Project Planning & System Architecture

### 1. What We Are Building
The architectural blueprint dividing the platform into decoupled tiers: React Frontend, FastAPI Backend, Browser Use Agent, n8n Orchestrator, and SQLite Database.

### 2. Why We Need It
Without a clean architectural division of responsibilities, AI projects quickly devolve into messy, unmaintainable scripts mixing scraping logic, API routes, and database code.

### 3. What Happens Internally
We design the **Dual Orchestration Pipeline**:
- **Macro Orchestration (n8n)**: Cron scheduling, webhook triggers, email digests.
- **Micro Execution (FastAPI + Browser Use)**: Headless browser automation, element selection, Pydantic extraction.
- **Fallback Guarantee**: If n8n is offline, FastAPI executes directly via internal `asyncio` background workers.

### 4. Files & Technologies Involved
- `docs/ARCHITECTURE.md`, `docs/architecture.md`.

### 5. Verification
Verify that every component has exactly one primary responsibility (Single Responsibility Principle).

---

## Phase 3: Technology Selection & Trade-Off Analysis

### 1. What We Are Building
Selecting the tech stack: React 18, Vite, Tailwind CSS, FastAPI, SQLite, Browser Use, Playwright, n8n, and OpenRouter.

### 2. Why We Need It
Every tool was chosen to optimize for developer velocity, reliability, and local zero-cost evaluation:
- **FastAPI** over Flask: Native async support and compile-time Pydantic validation.
- **SQLite** over PostgreSQL: Zero external daemon setup for instant local execution.
- **Browser Use** over BeautifulSoup: Renders modern JavaScript SPAs and handles dynamic search inputs.
- **n8n** over custom Python cron: Visual workflow debugging and decoupled email alerts.

### 3. Verification
Verify that all chosen technologies work cleanly on the target OS (macOS).

---

## Phase 4: Project Initialization & Environment Setup

### 1. What We Are Building
The core directory structure, virtual environments, dependency manifests, and environment templates.

### 2. Why We Need It
Ensures clean isolation, version locking, and prevents secrets from leaking into version control.

### 3. Files Created
- `backend/requirements.txt`: Specifying `fastapi`, `uvicorn`, `pydantic`, `httpx`, `browser-use`, `playwright`.
- `backend/.env.example` and `backend/.env`: Environment templates.
- `.gitignore`: Excluding `.venv/`, `node_modules/`, `.browseruse/`, `*.db`, and `.env`.

### 4. Verification
Run `python3 -c "import fastapi, browser_use, playwright; print('OK')"` and verify exit code 0.

---

## Phase 5: Database Modeling & Persistence Development

### 1. What We Are Building
The relational persistence layer managing opportunities, research runs, and user preferences.

### 2. Why We Need It
In-memory data vanishes when servers reboot. A relational store enables tracking application states over months.

### 3. What Happens Internally
- `backend/app/models/opportunity.py` defines schemas: `Opportunity`, `ResearchRun`, `UserPreferences`.
- `backend/app/database/db.py` creates tables with indexes:
  - `idx_opp_normalized_url` for $O(1)$ duplicate checking.
  - `idx_opp_status` and `idx_opp_type` for fast catalog filtering.

### 4. Verification
Run `init_db()` and check `sqlite3 backend/data/opportunities.db ".schema"`.

---

## 6. Phase 6: Normalization & Smart Deduplication Engine

### 1. What We Are Building
The URL cleaning and duplicate detection service in `backend/app/services/deduplication.py`.

### 2. Why We Need It
Aggregators cross-post identical jobs with different marketing UTM parameters. Re-scraping an already-saved opportunity should never erase the user's progress.

### 3. What Happens Internally
- `normalize_url()` uses `urllib.parse` to strip `utm_source`, `utm_medium`, `ref`, `fbclid`, and trailing slashes.
- `find_duplicate()` checks SQLite for existing matching URLs or fuzzy title/organization matches.
- **Status Preservation Guarantee**: If a match is found, refreshes `discovered_at` date, but **keeps the user's existing status** (`applied`, `saved`).

### 4. Verification
Automated test `test_04_deduplication_engine` verifies that an existing `APPLIED` listing never reverts to `NEW`.

---

## 7. Phase 7: Backend REST API Development

### 1. What We Are Building
FastAPI endpoints in `backend/app/api/endpoints.py` and application lifecycle manager in `backend/app/main.py`.

### 2. Why We Need It
Provides a clean, validated communication contract between the frontend, n8n, and backend workers.

### 3. Key Endpoints Built
- `GET /health`: Health ping.
- `POST /api/research`: Immediate HTTP 202 dispatch with background task worker.
- `GET /api/research/{run_id}`: Polling endpoint for frontend steppers.
- `GET /api/opportunities`: Search, category filtering, remote-only toggle, and pagination.
- `PATCH /api/opportunities/{id}`: Update application tracking status.
- `GET /api/workflows/status`: Diagnostics for n8n, Browser Use, and LLMs.
- `POST /api/webhooks/n8n/results`: Inbound callback receiver for n8n.

### 4. Verification
Run backend unit tests: `python3 -m unittest discover -s backend/tests -p "test_api.py" -v`.

---

## 8. Phase 8: AI & Browser Use Agent Integration

### 1. What We Are Building
The cognitive web agent in `backend/app/agents/browser_researcher.py`.

### 2. Why We Need It
Enables the application to navigate real opportunity websites autonomously.

### 3. What Happens Internally
- Sets `os.environ["BROWSER_USE_CONFIG_DIR"]` to local `.browseruse` to prevent OS permission errors.
- Configures `Browser(headless=True)`.
- Instantiates `ChatOpenRouter` or `ChatOpenAI`.
- Passes task instructions and `output_model_schema=OpportunityListOutput`.
- Implements `_generate_mock_opportunities` for instant, zero-cost development and testing.

### 4. Verification
Run `backend/tests/test_browser_agent.py` to verify schema conformance and mock generation.

---

## 9. Phase 9: n8n Workflow Automation Integration

### 1. What We Are Building
Three production-ready workflow definitions in `n8n/workflows/`:
1. `manual_opportunity_discovery.json`: On-demand webhook research pipeline.
2. `scheduled_opportunity_discovery.json`: 8:00 AM daily cron harvester.
3. `email_notifications.json`: HTML email digest with opportunity cards.

### 2. Why We Need It
Decouples macro-level scheduling, conditional alerting, and credential management from core Python code.

### 3. Verification
Test the inbound webhook using `curl -X POST http://127.0.0.1:8000/api/webhooks/n8n/results` with a sample payload.

---

## 10. Phase 10: React Frontend Dashboard Development

### 1. What We Are Building
Modern SaaS dashboard with Vite, React 18, Tailwind CSS, Lucide icons, and React Router.

### 2. Pages Created
- `DashboardPage.jsx`: 4 KPI metric cards, active execution status, integration diagnostics, recent discoveries.
- `DiscoverPage.jsx`: Multi-skill chips, custom tag input, opportunity types, location & experience, live 4-step execution stepper.
- `ResultsPage.jsx`: Filterable catalog with search bar, category tabs, and remote filter.
- `SavedPage.jsx`: Application pipeline manager (`Saved`, `Interested`, `Applied`, `Archived`).
- `SettingsPage.jsx`: Preference manager, n8n ping test, and safe credential diagnostics.
- `OpportunityCard.jsx`: Reusable card with inline status selector, deadline badges, and apply links.

### 3. Verification
Run `npm run build` in `frontend/` to verify zero compile or syntax errors.

---

## 11. Phase 11: End-to-End Integration & Polling Loop

### 1. What We Are Building
Connecting the frontend `api.js` client to the backend REST endpoints.

### 2. Why We Need It
Allows the user to click "Find Opportunities", see live stepper updates without freezing the browser, and inspect results as soon as the background worker commits to SQLite.

### 3. Verification
Trigger research on `/discover` and observe the live 4-step progress stepper advancing from Step 1 to Step 4.

---

## 12. Phase 12: Automated Testing & Quality Assurance

### 1. What We Are Building
Comprehensive test suite in `backend/tests/test_api.py` and `backend/tests/test_browser_agent.py`.

### 2. What Was Tested
- Health endpoints and system diagnostics.
- Input validation (rejecting `max_results > 50`).
- URL normalization and tracking parameter removal.
- Deduplication and Status Preservation Guarantee.
- Opportunity CRUD operations.
- Pydantic schema validation and mock generator accuracy.

### 3. Verification
Execute `python3 -m unittest discover -s backend/tests -p "test_*.py" -v`. (All 13 tests pass!).

---

## 13. Phase 13: Error Handling & Fault Tolerance Hardening

### 1. What We Are Building
Defensive safeguards across the entire stack:
- Missing API keys fall back gracefully to the mock engine with explicit UI banners.
- Offline n8n instances trigger automatic fallback to direct FastAPI background tasks.
- Navigation timeouts (`step_timeout=120`, `max_failures=3`) prevent hanging processes.
- Directory auto-creation (`mkdir(parents=True)`) prevents file system crashes.

---

## 14. Phase 14: Documentation & Interview Preparation

### 1. What We Are Building
The comprehensive documentation suite in `/docs` and `/project-documentation`:
- Architecture guides, tech stack deep dives, file walkthroughs, troubleshooting handbooks, interview Q&A, and demo scripts.

---

## 15. Phase 15: Production Deployment Strategy

### 1. Local Deployment (Current)
Run backend with `uvicorn`, frontend with `vite`, and n8n with `npx n8n`.

### 2. Cloud Production Deployment Roadmap
- **Containerization**: Multi-stage `Dockerfile` for FastAPI backend and static Nginx container for React build.
- **Database**: Managed PostgreSQL on AWS RDS or Supabase.
- **Worker Queue**: Celery or ARQ with Redis broker for asynchronous browser tasks.
- **Browser Cluster**: Connect Browser Use to Browserbase or a cloud Playwright container cluster.
- **Reverse Proxy**: Nginx or Traefik with automated Let's Encrypt SSL/TLS certificates.

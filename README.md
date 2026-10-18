# 🎯 Opportunity Hunter AI

> **An autonomous opportunity discovery agent that helps students find internships, hackathons, research opportunities, and entry-level jobs based on their skills, interests, and preferences.**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.142.2-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.3-61DAFB?logo=react)](https://react.dev)
[![Vite](https://img.shields.io/badge/Vite-5.4-646CFF?logo=vite)](https://vitejs.dev)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4-38B2AC?logo=tailwind-css)](https://tailwindcss.com)
[![Browser Use](https://img.shields.io/badge/Browser_Use-0.13.10-FF5722)](https://github.com/browser-use/browser-use)
[![n8n](https://img.shields.io/badge/n8n-Orchestration-FF6D5A?logo=n8n)](https://n8n.io)
[![Tests](https://img.shields.io/badge/Tests-13%20Passed-brightgreen)](backend/tests/)

Opportunity Hunter AI is a genuine browser automation and workflow orchestration system—not simply a text-only chatbot. It combines **Playwright-driven Browser Use Web AI**, **n8n workflow automation**, an asynchronous **FastAPI backend with SQLite persistence**, and a modern **React 18 SaaS dashboard**.

---

## 🌟 Key Features

- 🤖 **Browser Use Web AI Agent**: Navigates opportunity websites (Devpost, Y Combinator jobs, GitHub, etc.), identifies matching positions, extracts structured data, and enforces strict schema validation.
- 🔄 **Dual Orchestration Pipeline**:
  - **n8n Workflows**: Importable workflows for manual research webhooks, scheduled daily cron harvesting, and formatted HTML email digests.
  - **Direct Background Runner**: Built-in Python `asyncio` runner allowing immediate local testing even without an active n8n instance.
- ⚡ **URL Normalization & Smart Deduplication**: Normalizes tracking parameters (`utm_*`, `ref`, `fbclid`), detects duplicates via URL and fuzzy title/organization matching, and **preserves user application status** (e.g. `saved`, `applied`).
- 🎨 **Polished SaaS Dashboard**:
  - **Dashboard**: Overview KPIs, active research run status, agent health diagnostics, and recent discoveries.
  - **Discover**: Dynamic skills selector, opportunity types pills, location/experience settings, and live multi-step execution progress.
  - **Opportunity Results**: Filterable catalog with search, category tabs, remote filters, and instant status updates.
  - **Saved & Applications**: Kanban/table tracker to advance opportunities from Saved to Applied or Archived.
  - **Settings**: Preference management, n8n webhook health ping, and safe LLM credential diagnostics.
- 🛡️ **Zero-Cost Mock Mode**: Includes an intelligent mock research engine for offline development and local evaluation without consuming LLM credits.
- 🔒 **Security First**: API keys and secrets remain strictly in backend `.env` variables and are never leaked to client bundles.

---

## 🏗️ Architecture

```
React Dashboard (Vite + Tailwind)
       │
       ▼
FastAPI Backend (Pydantic v2 + SQLite)
       │
       ▼
n8n Webhook Trigger (Optional)
       │
       ▼
Browser Use Research Agent (Playwright Chromium)
       │
       ▼
Structured Opportunities (OpportunityListOutput)
       │
       ▼
Deduplication & Storage Engine
       │
       ▼
React Dashboard + Email Notification Digest
```

---

## 📁 Project Structure

```
opp-hunter/
├── frontend/                     # React 18 + Vite + Tailwind CSS dashboard
│   ├── src/
│   │   ├── components/           # Navbar, Sidebar, OpportunityCard
│   │   ├── pages/                # Dashboard, Discover, Results, Saved, Settings
│   │   ├── services/             # Axios/Fetch API client
│   │   ├── App.jsx               # React Router container
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── backend/                      # Python FastAPI backend
│   ├── app/
│   │   ├── main.py               # Application entrypoint & CORS
│   │   ├── api/                  # REST endpoints & webhook receivers
│   │   ├── models/               # Pydantic schemas (Opportunity, Run, Prefs)
│   │   ├── database/             # SQLite connection & CRUD queries
│   │   ├── services/             # URL normalization & deduplication
│   │   └── agents/               # Browser Use agent & mock engine
│   ├── tests/                    # Automated unit & integration tests
│   ├── requirements.txt
│   └── .env.example
│
├── n8n/                          # n8n Orchestration Workflows
│   ├── workflows/
│   │   ├── manual_opportunity_discovery.json
│   │   ├── scheduled_opportunity_discovery.json
│   │   └── email_notifications.json
│   └── README.md                 # Import & setup guide
│
├── docs/                         # Technical documentation
│   ├── architecture.md           # System design & algorithms
│   └── setup-guide.md            # Step-by-step local launch instructions
│
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start (Local Launch)

### 1. Start the FastAPI Backend
In your first terminal:

```bash
# Optional: create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Start backend server
python3 -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

The API will be live at `http://127.0.0.1:8000` with interactive Swagger docs at `http://127.0.0.1:8000/docs`.

---

### 2. Start the React Frontend
In your second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open your browser at `http://localhost:5173`.

---

### 3. (Optional) Run n8n Workflows
In a third terminal:

```bash
npx n8n
```
1. Open `http://localhost:5678` in your browser.
2. Import the workflows from `n8n/workflows/`.
3. Set `N8N_INTEGRATION_ENABLED=true` in `backend/.env`.

---

## 🧪 Running Automated Tests

Run the test suite to verify endpoints, schema validation, URL normalization, and deduplication:

```bash
python3 -m unittest discover -s backend/tests -p "test_*.py" -v
```

**Test Coverage Summary:**
- `test_01_health_check`: Health endpoint verification (`GET /health`).
- `test_02_workflow_status`: System diagnostics and service status.
- `test_03_url_normalization`: Stripping tracking tokens, sorting params, lowercase host.
- `test_04_deduplication_engine`: Duplicate matching while preserving user `APPLIED` status.
- `test_05_research_request_validation`: Pydantic range checking on request limits.
- `test_06_trigger_research_mock_mode`: Asynchronous run initiation and run polling.
- `test_07_n8n_webhook_results_receiver`: Inbound webhook results processing.
- `test_08_opportunities_crud`: Listing, filtering, updating, and deleting records.
- `test_09_user_preferences`: Preference read/write persistence.
- `test_browser_agent`: Schema conformance and mock opportunity generator.

---

## 🔌 REST API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Service health status |
| `GET` | `/api/workflows/status` | Diagnostics for n8n, Browser Use, and LLM |
| `GET` | `/api/dashboard/stats` | Aggregated opportunity statistics |
| `POST` | `/api/research` | Trigger opportunity discovery run |
| `GET` | `/api/research/{run_id}` | Poll research run status |
| `POST` | `/api/browser-use/execute`| Direct browser agent execution (called by n8n) |
| `GET` | `/api/opportunities` | List and filter opportunities |
| `GET` | `/api/opportunities/{id}` | Get single opportunity |
| `PATCH` | `/api/opportunities/{id}` | Update opportunity status |
| `DELETE`| `/api/opportunities/{id}` | Remove opportunity |
| `GET` | `/api/preferences` | Retrieve user preferences |
| `PUT` | `/api/preferences` | Update user preferences |
| `POST` | `/api/webhooks/n8n/results`| Inbound webhook from n8n |

---

## 📄 License & Ethical Automation Note

This project is built for educational, portfolio, and personal career development purposes. When running live browser research, always respect target websites' terms of service, robots restrictions, and rate limits. Opportunity Hunter AI does not bypass CAPTCHAs, perform credential stuffing, or submit automated applications.

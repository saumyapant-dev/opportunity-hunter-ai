# Opportunity Hunter AI - Local Setup & Launch Guide

Step-by-step instructions to launch Opportunity Hunter AI locally.

---

## Prerequisites

1. **Python 3.11+** (FastAPI, SQLite, Playwright, Browser Use)
2. **Node.js 18+ and npm** (Vite, React 18, Tailwind CSS)
3. **n8n** (Optional for workflow orchestration, or run via `npx n8n`)

---

## 1. Backend Setup

### A. Install Python Dependencies
From the project root:

```bash
pip install -r backend/requirements.txt
```

### B. Configure Environment Variables
Copy `.env.example` to `backend/.env`:

```bash
cp backend/.env.example backend/.env
```

To enable live AI research with OpenRouter or OpenAI, add your API key in `backend/.env`:
```ini
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=your_openrouter_api_key_here
LLM_MODEL=meta-llama/llama-3.3-70b-instruct
```

> **Note**: If no API key is provided, the platform automatically runs in **Mock Engine Mode**, providing high-fidelity simulated listings without consuming any API credits.

### C. Launch FastAPI Backend
```bash
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

Verify backend health:
```bash
curl http://127.0.0.1:8000/health
```

---

## 2. Frontend Setup

### A. Install Node Dependencies
In a new terminal window:

```bash
cd frontend
npm install
```

### B. Launch Vite Dev Server
```bash
npm run dev
```

Open your browser and navigate to:
```
http://localhost:5173
```

---

## 3. n8n Workflow Orchestration (Optional & Recommended)

### A. Start n8n
In a separate terminal:
```bash
npx n8n
```
The n8n editor opens at `http://localhost:5678`.

### B. Import Workflows
1. Click **Workflows** -> **+ Add Workflow**.
2. Click the top-right menu `...` -> **Import from File**.
3. Import the files from `n8n/workflows/`:
   - `manual_opportunity_discovery.json`
   - `scheduled_opportunity_discovery.json`
   - `email_notifications.json`
4. Toggle each workflow to **Active**.

### C. Enable n8n in Backend `.env`
In `backend/.env`, set:
```ini
N8N_INTEGRATION_ENABLED=true
N8N_WEBHOOK_URL=http://localhost:5678/webhook/opportunity-research
```

---

## 4. Running Automated Tests

Run the full backend test suite:
```bash
python3 -m unittest discover -s backend/tests -p "test_*.py" -v
```

All 13 tests covering endpoints, URL deduplication, Pydantic schemas, and mock generation should pass.

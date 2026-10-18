# Opportunity Hunter AI — Live Demonstration Script

This script provides an exact, step-by-step guide for demonstrating **Opportunity Hunter AI** to an interviewer, hiring manager, or technical evaluator.

---

## Preparation Checklist Before the Interview
- [ ] Open Terminal 1: Start FastAPI backend (`uvicorn backend.app.main:app --port 8000`).
- [ ] Open Terminal 2: Start React frontend (`npm run dev` in `frontend/`).
- [ ] Open Browser Tab 1: Navigate to `http://localhost:5173` (React Dashboard).
- [ ] Open Browser Tab 2: Navigate to `http://localhost:8000/docs` (Swagger API Docs).
- [ ] (Optional) Open Browser Tab 3: Navigate to `http://localhost:5678` (n8n Webhook Canvas).

---

## 10-Step Live Demonstration Walkthrough

### 1. Introduce the Problem (30 seconds)
- **Action**: Display the Dashboard on `http://localhost:5173`.
- **Script**:
  > *"To start, I want to briefly highlight the problem Opportunity Hunter AI solves. As computer science students, we waste hours every week checking disconnected portals—Devpost for hackathons, Hacker News and startup boards for internships, and university sites for research. Information is scattered, duplicate listings are common, and deadlines pass unnoticed.*
  >
  > *I built Opportunity Hunter AI to automate this entire pipeline: deploying an autonomous AI browser agent that navigates live websites, extracts verified listings into a persistent database, and tracks applications directly inside a centralized dashboard."*

---

### 2. Demonstrate the Dashboard (30 seconds)
- **Action**: Hover over the KPI cards and System Integration widget.
- **Script**:
  > *"Here on the main dashboard, we see real-time career analytics: Total Opportunities Discovered, New Opportunities awaiting review, Bookmarked listings, and Applications Tracked. On the right, our diagnostic widget actively verifies system health—confirming that our Playwright browser engine is ready, checking our LLM configuration, and probing n8n workflow connectivity."*

---

### 3. Configure User Preferences (30 seconds)
- **Action**: Click **Settings** in the sidebar.
- **Script**:
  > *"In Settings, students configure their default discovery profile: preferred locations (e.g. Remote), notification email addresses, and daily cron expressions (default: 8:00 AM daily). When saved, these are committed to SQLite and read automatically by our scheduled n8n workflows."*

---

### 4. Trigger Opportunity Discovery (45 seconds)
- **Action**: Click **Discover Opportunities** in the sidebar. Select `Python`, `React`, and type `FastAPI` in the custom box. Toggle `Internship` and `Hackathon`. Ensure mode is set to `Mock` (or `Live AI`). Click **"Find Opportunities Now"**.
- **Script**:
  > *"Now let's launch a discovery run. I've selected Python, React, and FastAPI. The moment I click 'Find Opportunities', the FastAPI backend validates the payload via Pydantic and returns an HTTP 202 Accepted status in milliseconds with a unique run ID. This is a non-blocking architecture—the UI remains responsive while the execution stepper polls status in the background."*

---

### 5. Explain the Browser Automation Process (45 seconds)
- **Action**: Point to the 4-step progress stepper advancing from Step 1 to Step 4.
- **Script**:
  > *"While this runs, our agent service in the backend launches a headless Chromium instance via Playwright. Browser Use converts the webpage DOM into an accessibility tree, pruning layout noise. An LLM reasons over the interactive nodes, navigates search forms, and extracts structured listings conforming to our Pydantic schema. Missing deadlines are strictly set to null to prevent hallucinations."*

---

### 6. Review Results & Demonstrate Opportunity Matching (45 seconds)
- **Action**: Scroll down to the newly rendered opportunity cards.
- **Script**:
  > *"The run has completed, discovering fresh opportunities matching our exact criteria. Notice the cards: verified titles, host organizations, remote badges, skill pills, and direct apply links.*
  >
  > *Before reaching this screen, every listing passed through our deduplication engine in `deduplication.py`. We strip UTM marketing tokens and check existing records. If an opportunity was already marked as 'applied' by the student, re-discovering it refreshes the timestamp without overwriting their application status."*

---

### 7. Demonstrate the Application Tracker (30 seconds)
- **Action**: On one card, click the **Bookmark** icon. On another, change the status dropdown to **Applied**. Click **Saved & Applications** in the sidebar.
- **Script**:
  > *"Students can manage their entire application lifecycle right here. When I change the status to 'Applied', an asynchronous PATCH request updates SQLite. Navigating to the Saved page allows us to filter applications by stage: Saved, Interested, Applied, and Archived."*

---

### 8. Demonstrate n8n Workflows (30 seconds)
- **Action**: Switch briefly to the n8n canvas or reference the `n8n/workflows/` directory.
- **Script**:
  > *"To automate daily harvesting, I integrated n8n. Workflow 2 triggers every morning at 8:00 AM, fetches user preferences from our FastAPI REST API, runs the agent, stores new records, and dispatches an HTML email digest of newly discovered openings to the student's inbox."*

---

### 9. Explain the Backend & Database (30 seconds)
- **Action**: Open `http://127.0.0.1:8000/docs` (Swagger UI).
- **Script**:
  > *"Here in our FastAPI Swagger documentation, you can see our complete RESTful contract: health checks, research dispatchers, paginated opportunity catalogs, and inbound n8n webhook receivers. Everything is backed by SQLite with B-tree indexes on normalized URLs for logarithmic lookup speeds."*

---

### 10. Conclude with Limitations & Future Improvements (30 seconds)
- **Action**: Return to the main dashboard.
- **Script**:
  > *"To conclude: Opportunity Hunter AI demonstrates end-to-end full-stack AI engineering. In terms of future scaling, the architecture is ready to migrate from SQLite to distributed PostgreSQL on RDS, replace in-process background tasks with Celery/Redis worker queues, and connect to remote browser grids like Browserbase for multi-tenant scalability. Thank you, and I'd love to answer any questions!"*

---

## Questions an Interviewer Might Ask During the Demo

1. *"Why did you use mock mode during this demo?"*
   - **Answer**: *"To demonstrate deterministic, zero-latency execution without consuming live LLM API credits or risking venue Wi-Fi timeouts. The live mode uses the identical Pydantic schema and agent loop."*
2. *"What happens if a website detects and blocks the headless browser?"*
   - **Answer**: *"The agent catches the navigation failure, logs it defensively, and falls back to our mock engine with explicit UI banners, ensuring the server never crashes."*
3. *"Why didn't you use WebSockets for the live stepper?"*
   - **Answer**: *"For short-lived 15–30 second background tasks, lightweight HTTP polling (1.2-second interval) provides an identical user experience with significantly lower server connection overhead than persistent WebSockets."*

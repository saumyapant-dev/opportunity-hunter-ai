# Opportunity Hunter AI — Practical Learning Roadmap (11 Modules)

A structured, beginner-friendly curriculum designed to teach you how to build, explain, and customize **Opportunity Hunter AI** step by step.

---

## Module 1: The Problem Space & AI Agent Fundamentals
- **Concepts to Learn**: Information fragmentation in job discovery, traditional scrapers vs. AI agents, the Perception-Action loop, structured data extraction.
- **Relevant Files to Study**: `docs/PROJECT_OVERVIEW.md`, `README.md`.
- **Practical Exercise**: Manually search for "Python internships" on Devpost and Hacker News. Note how many clicks it takes, how many expired listings you find, and how inconsistent the formatting is.
- **Expected Outcome**: Clear, intuitive understanding of why automated agentic discovery is valuable.
- **Common Beginner Mistakes**: Thinking an AI agent is just a chatbot like ChatGPT, without realizing an agent takes real actions in external environments.
- **Independent Task**: Write down your own 30-second elevator pitch explaining what problem Opportunity Hunter AI solves.

---

## Module 2: High-Level Project Architecture
- **Concepts to Learn**: Client-server architecture, decoupled orchestration, micro-execution vs. macro-orchestration, synchronous vs. asynchronous I/O.
- **Relevant Files to Study**: `docs/ARCHITECTURE.md`.
- **Practical Exercise**: Trace the path of an opportunity from target website DOM $\rightarrow$ Playwright $\rightarrow$ Browser Use $\rightarrow$ FastAPI $\rightarrow$ SQLite $\rightarrow$ React UI.
- **Expected Outcome**: Ability to draw and explain the system architecture on a whiteboard.
- **Common Beginner Mistakes**: Believing that React directly communicates with SQLite or Browser Use without an intermediary backend API.
- **Independent Task**: Sketch the sequence diagram on paper from memory without looking at the documentation.

---

## Module 3: Development Environment Setup
- **Concepts to Learn**: Node.js & npm package management, Python virtual environments, pip dependency manifests, environment variables (`.env`).
- **Relevant Files to Study**: `backend/requirements.txt`, `backend/.env.example`, `frontend/package.json`.
- **Practical Exercise**: Clone the repository, copy `.env.example` to `.env`, and run `python3 -m pip install -r backend/requirements.txt`.
- **Expected Outcome**: A fully configured local environment with all Python and Node dependencies installed.
- **Common Beginner Mistakes**: Hardcoding API keys directly into Python files instead of using environment variables.
- **Independent Task**: Add a custom variable `PROJECT_CODENAME="hunter_v1"` to `backend/.env` and print it in Python using `os.getenv()`.

---

## Module 4: Building the React Dashboard
- **Concepts to Learn**: React components, Props, State (`useState`), Effects (`useEffect`), Tailwind CSS utility classes, React Router navigation.
- **Relevant Files to Study**: `frontend/src/App.jsx`, `frontend/src/pages/DiscoverPage.jsx`, `frontend/src/components/OpportunityCard.jsx`.
- **Practical Exercise**: Open `DiscoverPage.jsx`, add a new preset skill button (e.g., `"Docker"` or `"Kubernetes"`), and verify it toggles cleanly in the UI.
- **Expected Outcome**: Mastery of building interactive modern dashboards with Tailwind CSS.
- **Common Beginner Mistakes**: Mutating React state directly (`state.push(item)`) instead of using setter functions (`setState([...state, item])`).
- **Independent Task**: Add a new filter badge in `OpportunityCard.jsx` that displays "New Posting" if the listing was discovered within the last 24 hours.

---

## Module 5: Building the FastAPI Backend & REST APIs
- **Concepts to Learn**: ASGI servers (`uvicorn`), HTTP verbs (`GET`, `POST`, `PATCH`, `DELETE`), HTTP status codes (`200`, `202`, `404`, `422`), Pydantic validation, CORS middleware.
- **Relevant Files to Study**: `backend/app/main.py`, `backend/app/api/endpoints.py`, `backend/app/models/opportunity.py`.
- **Practical Exercise**: Open your browser to `http://127.0.0.1:8000/docs` and use the interactive Swagger UI to trigger `/api/opportunities` and `/health`.
- **Expected Outcome**: Complete confidence in creating, modifying, and testing REST API endpoints.
- **Common Beginner Mistakes**: Returning blocking synchronous responses for tasks that take 30+ seconds, causing gateway timeouts.
- **Independent Task**: Create a new endpoint `GET /api/stats/skills` that returns the count of opportunities requiring each skill.

---

## Module 6: Designing the Database & Deduplication
- **Concepts to Learn**: Relational database schemas, B-tree indexes, ACID transactions, URL normalization, idempotent upserts, status preservation.
- **Relevant Files to Study**: `backend/app/database/db.py`, `backend/app/services/deduplication.py`.
- **Practical Exercise**: Open the database directly using `sqlite3 backend/data/opportunities.db` and run SQL queries: `SELECT title, organization, status FROM opportunities;`.
- **Expected Outcome**: Understanding how to store and query relational data securely using parameterized SQL.
- **Common Beginner Mistakes**: Writing string-concatenated SQL queries (`f"SELECT * WHERE id = '{id}'"`), which opens the door to SQL Injection attacks.
- **Independent Task**: Write a test verifying that `normalize_url("https://site.com/jobs/?utm_campaign=spring&ref=campus")` returns `"https://site.com/jobs"`.

---

## Module 7: Integrating the LLM (OpenRouter / OpenAI)
- **Concepts to Learn**: LLM prompting, function calling, constrained JSON decoding, temperature, prompt grounding.
- **Relevant Files to Study**: `backend/app/agents/browser_researcher.py`, `backend/app/models/opportunity.py`.
- **Practical Exercise**: Inspect `OpportunityListOutput`. Notice how each field description instructs the model to return `null` instead of guessing.
- **Expected Outcome**: Knowing how to extract clean, typed JSON from an LLM without conversational filler.
- **Common Beginner Mistakes**: Allowing LLMs to return free-form markdown text and attempting to parse it with brittle regular expressions.
- **Independent Task**: Update the prompt in `browser_researcher.py` to also look for compensation or stipend details if explicitly mentioned on the page.

---

## Module 8: Implementing Browser Use Web AI
- **Concepts to Learn**: Headless browser automation, Playwright Chromium, accessibility tree pruning, element indexing, perception-action loops.
- **Relevant Files to Study**: `backend/app/agents/browser_researcher.py`.
- **Practical Exercise**: Run a live search in `Live AI` mode with `BROWSER_USE_HEADLESS=false` in `.env` to watch the browser navigate and click in real time!
- **Expected Outcome**: Deep understanding of how an AI agent actually controls a browser.
- **Common Beginner Mistakes**: Running headless browsers with unrestricted profile paths, causing OS directory permission errors.
- **Independent Task**: Modify the `max_steps` parameter and observe how it affects the agent's exploration depth.

---

## Module 9: Building n8n Workflows
- **Concepts to Learn**: Node-based automation, Webhook triggers, Schedule triggers, Code nodes (JavaScript), HTTP Request nodes, Send Email nodes.
- **Relevant Files to Study**: `n8n/workflows/manual_opportunity_discovery.json`, `n8n/workflows/scheduled_opportunity_discovery.json`, `n8n/workflows/email_notifications.json`.
- **Practical Exercise**: Launch n8n via `npx n8n`, import the 3 JSON files, and test the webhook node with a test payload.
- **Expected Outcome**: Ability to design, import, and troubleshoot automated workflows in n8n.
- **Common Beginner Mistakes**: Hardcoding email passwords inside exported workflow JSON files instead of using n8n's encrypted Credential Store.
- **Independent Task**: Add a Discord or Slack notification node to the scheduled discovery workflow.

---

## Module 10: Connecting All Components End-to-End
- **Concepts to Learn**: Non-blocking asynchronous polling, Vite API proxies, error handling fallbacks, optimistic UI updating.
- **Relevant Files to Study**: `frontend/src/services/api.js`, `frontend/src/pages/DiscoverPage.jsx`, `backend/app/api/endpoints.py`.
- **Practical Exercise**: Start the backend, start the frontend, execute a search on `/discover`, and watch the 4-step stepper advance in real time.
- **Expected Outcome**: Full comprehension of the end-to-end data flow from user click to database commit and UI render.
- **Common Beginner Mistakes**: Forgetting to configure CORS, leading to browser `Access-Control-Allow-Origin` errors.
- **Independent Task**: Test the automatic fallback by stopping n8n and verifying that research still succeeds via the internal runner.

---

## Module 11: Testing, Debugging & Interview Defense
- **Concepts to Learn**: Unit testing, integration testing, test fixtures, defensive error logging, technical interview pitch delivery.
- **Relevant Files to Study**: `backend/tests/test_api.py`, `backend/tests/test_browser_agent.py`, `docs/INTERVIEW_PREPARATION.md`.
- **Practical Exercise**: Run the complete automated test suite: `python3 -m unittest discover -s backend/tests -p "test_*.py" -v`.
- **Expected Outcome**: Complete readiness to demonstrate, defend, and answer questions about this project in technical interviews.
- **Common Beginner Mistakes**: Claiming the project is "100% bug-free and infinitely scalable" instead of objectively discussing architectural trade-offs.
- **Independent Task**: Practice the 2-minute technical pitch from `docs/PROJECT_PITCH.md` out loud until you can deliver it without notes.

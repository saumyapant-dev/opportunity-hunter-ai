# Opportunity Hunter AI — Project Pitches

Verbal scripts customized for technical interviews, portfolio presentations, and recruiter screenings.

---

## 1. The 30-Second Elevator Pitch
> *"I built **Opportunity Hunter AI**, an autonomous opportunity discovery agent that helps students find internships, hackathons, and research fellowships tailored to their exact skill set. Unlike brittle scrapers that break when website CSS changes, it uses Browser Use Web AI to control a Playwright Chromium browser like a human, extracting structured listings via an LLM. I paired it with an asynchronous FastAPI backend, SQLite with automated URL deduplication, and n8n workflow automation for daily 8 AM cron harvesting and email digests. It completely automates the tedious early-career job hunt."*

---

## 2. The 1-Minute Project Explanation
> *"As a computer science student, I experienced firsthand how chaotic and fragmented early-career opportunity discovery is. High-value internships, hackathons, and research grants are scattered across Devpost, Hacker News, and startup portals, often buried under senior roles or expired deadlines. To solve this, I designed and built **Opportunity Hunter AI**.*
>
> *The system features a modern React dashboard where students select their technical skills and target categories. When a search is triggered, our FastAPI backend initiates an autonomous Browser Use agent controlling a headless Playwright browser. The agent evaluates dynamic web pages, navigates interactive search forms, and extracts structured listings conforming to Pydantic schemas.*
>
> *Results pass through a custom deduplication engine that strips tracking parameters and enforces a 'status preservation guarantee' so existing applications are never clobbered. I also integrated n8n to handle daily 8 AM scheduled harvesting and send formatted HTML email digests. The entire project is fully tested with 13 automated tests and includes a zero-cost mock mode for offline development."*

---

## 3. The 3-Minute Technical Walkthrough
Use this version when an interviewer says: *"Tell me about a complex project you built and walk me through the architecture."*

### Step 1: The Problem & Architectural Motivation (45 seconds)
> *"I built Opportunity Hunter AI to address the architectural limitations of traditional web scraping for career discovery. Traditional BeautifulSoup or cURL scrapers fail on modern Single Page Applications (SPAs) because they cannot execute client-side JavaScript, navigate dynamic search forms, or handle infinite scroll pagination. I wanted to build a genuine autonomous agent that perceives web interfaces semantically while maintaining strict data integrity."*

### Step 2: High-Level Architecture & Agentic Loop (60 seconds)
> *"The application is architected across four decoupled tiers:*
>
> *On the frontend, I used React 18, Vite, and Tailwind CSS to build a responsive dashboard with an interactive search console, live progress steppers, and an application pipeline tracker.*
>
> *When a student triggers research, the request hits a FastAPI REST backend. Because browser automation takes 15 to 45 seconds, the endpoint returns an HTTP 202 Accepted status in milliseconds with a unique run ID, offloading the task to an asynchronous background worker pool. This allows the frontend to poll status non-blockingly without risking gateway timeouts.*
>
> *In the background, our agent service launches Browser Use Web AI on top of Playwright Chromium. The agent converts target web pages into a compact accessibility tree, feeds the semantic context into an LLM via OpenRouter or OpenAI, and extracts structured listings strictly validated against our Pydantic `OpportunityListOutput` schema. Missing deadlines are explicitly stored as null—preventing hallucinations."*

### Step 3: Deduplication, Workflow Orchestration & Resilience (45 seconds)
> *"Before persisting to our SQLite database, listings pass through a custom deduplication engine. We strip marketing tokens like UTM parameters and perform fuzzy title and company matching. A critical engineering decision was implementing a 'status preservation guarantee'—if a student already marked an internship as 'applied', re-discovering it refreshes the date without reverting their application progress.*
>
> *To decouple macro-level scheduling from core agent code, I integrated n8n. Workflow 2 triggers every morning at 8:00 AM, reads user preferences from our API, runs the agent, and dispatches an HTML email digest of newly discovered openings.*
>
> *Finally, I engineered multi-tier fault tolerance: if an external site times out or an LLM key expires, the system catches the error, logs it defensively, and falls back to our high-fidelity mock engine with clear diagnostics."*

### Step 4: Closing & Impact (30 seconds)
> *"The project is thoroughly verified with 13 automated unit and integration tests covering health, deduplication, schema validation, and CRUD operations. It demonstrates end-to-end full-stack AI engineering: combining autonomous browser control, asynchronous Python APIs, robust data normalization, and workflow orchestration. I'd be excited to dive deeper into any part of the implementation!"*

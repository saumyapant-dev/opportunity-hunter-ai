# Opportunity Hunter AI — Technical Interview Preparation & Defense

This guide equips you to confidently present, explain, and defend **Opportunity Hunter AI** in technical interviews for Software Engineering, Full-Stack, and AI Agent roles.

---

## 1. Core Architectural & Design Decisions

### Q1. Why did you choose this multi-tier architecture?
- **Interview Answer**: *"I chose a decoupled multi-tier architecture—React for presentation, FastAPI for REST APIs and data validation, Browser Use for autonomous web perception, and n8n for workflow orchestration—to enforce the Single Responsibility Principle. Mixing browser automation, scheduling, database queries, and UI logic in a single monolithic script would create an unmaintainable codebase. By decoupling the layers, I can swap the frontend for mobile, switch SQLite to PostgreSQL, or change LLM providers without touching the other tiers."*

---

### Q2. Why use FastAPI instead of Express.js?
- **Interview Answer**: *"While Express is popular for JavaScript backends, FastAPI was the superior choice here for three specific reasons: 1) The entire AI agent ecosystem—Browser Use, Playwright Python, LangChain, and Pydantic—is natively developed in Python; 2) FastAPI provides automatic compile-time validation via Pydantic v2, eliminating hundreds of lines of manual input checking; and 3) Native async/await event loops allow non-blocking execution while managing long-running browser processes."*

---

### Q3. Why use n8n instead of writing every automation in Python?
- **Interview Answer**: *"Separation of concerns. Writing custom cron schedulers, email template assemblers, and retry logic in pure Python adds operational boilerplate. n8n acts as an event-driven macro-orchestrator: it provides visual execution logs, handles daily 8 AM scheduling, and manages encrypted SMTP credentials. If a non-technical recruiter wants to tweak the email template or route alerts to Slack, they can do so in n8n's visual canvas without redeploying backend code."*

---

### Q4. Why use Browser Use instead of ordinary web scraping?
- **Interview Answer**: *"Ordinary scraping with BeautifulSoup or requests works by parsing static HTML. Modern career portals (Devpost, Y Combinator, Lever, Greenhouse) are dynamic React/Vue Single Page Applications that rely on client-side JavaScript rendering, interactive search inputs, and infinite scrolling. Browser Use controls a real Playwright Chromium browser, understands the accessibility tree like a human, and navigates multi-step forms autonomously, making it resilient to website class-name changes."*

---

### Q5. Why use SQLite instead of PostgreSQL or MongoDB?
- **Interview Answer**: *"For a local, single-user developer tool, SQLite is unbeatable: it is embedded directly in Python, stores all data in a single file (`opportunities.db`), requires zero external Docker daemon or cloud database setup, and provides full ACID transaction guarantees. In my system design analysis, I have already mapped out the migration path to PostgreSQL with connection pooling (PgBouncer) for multi-tenant production scaling."*

---

### Q6. How does the system avoid duplicate opportunities?
- **Interview Answer**: *"We implement a two-stage deduplication pipeline: First, deterministic URL normalization strips all marketing tokens (`utm_*`, `ref`, `source`, `fbclid`), standardizes casing, default ports, and removes trailing slashes. Second, we query an indexed lookup in SQLite on `normalized_url` with a fallback to fuzzy title and organization matching. Crucially, we enforce a 'Status Preservation Guarantee'—if an opportunity was previously marked as 'applied' or 'saved' by the user, re-discovering it refreshes the date without overwriting the user's application status."*

---

### Q7. How do you handle failed browser automation or website timeouts?
- **Interview Answer**: *"Defensively across three layers: 1) At the browser layer, we configure `max_failures=3` and `step_timeout=120` seconds so slow pages don't hang indefinitely; 2) In the agent service, all live calls are wrapped in exception handlers that catch network errors, log the issue, and activate our built-in fallback engine; 3) At the API layer, runs that encounter unrecoverable errors update the database status to `FAILED` with an explicit error message, preventing the user interface from being left in a permanent loading state."*

---

### Q8. How do you prevent invalid or hallucinated opportunity information?
- **Interview Answer**: *"1) Strict schema enforcement: We pass `output_model_schema=OpportunityListOutput` to the agent, forcing the LLM to output typed Pydantic models via function calling; 2) Explicit negative prompting: The prompt strictly instructs: 'If a deadline is not explicitly present on the page, set it to null. Never invent deadlines or links.'; 3) Backend post-validation: The backend verifies that extracted application URLs use valid HTTP schemes and actually point to the source domain."*

---

### Q9. How would you scale this application for thousands of users?
- **Interview Answer**: *"I would execute a 4-part scaling roadmap: 1) Database: Migrate SQLite to distributed PostgreSQL on RDS with Row-Level Security for multi-tenant isolation; 2) Task Queues: Replace in-process `BackgroundTasks` with Celery and Redis to distribute browser jobs across worker nodes; 3) Remote Browser Pools: Offload Chromium instances to a managed browser grid like Browserbase to prevent server RAM exhaustion; 4) Event Streaming: Replace 1.2-second HTTP polling with WebSockets or Server-Sent Events (SSE) for real-time progress updates."*

---

### Q10. What would you improve if you had more development time?
- **Interview Answer**: *"I would implement three major enhancements: 1) User Authentication: Add OAuth2 (Google/GitHub login) to support personalized multi-user profiles; 2) Relevance Scoring: Implement semantic vector embeddings (using SentenceTransformers) to rank opportunities by similarity against a student's uploaded PDF resume; 3) Automated Deadline Alerts: A background daemon that alerts students 48 hours before an application deadline expires."*

---

## 2. Technical Interview Questions & Answers

### Frontend (React & Modern Web)
- **Q: Why use non-blocking polling on the Discover page instead of holding the HTTP request open?**
  - *Answer*: Browser automation takes 15 to 45 seconds. Holding an HTTP request open risks gateway timeouts (504 Gateway Timeout) from reverse proxies like Nginx or Cloudflare. Returning an HTTP 202 immediately and polling status asynchronously decouples client request lifecycles from long-running background tasks.
- **Q: How does Vite proxy resolve CORS issues in development?**
  - *Answer*: In `vite.config.js`, the proxy intercepts requests sent to `/api` and forwards them to `http://127.0.0.1:8000`. Because the browser thinks it is communicating with the same origin (`localhost:5173`), browser CORS restrictions are completely bypassed during local development.

### Backend (FastAPI & Python)
- **Q: What is the difference between synchronous `def` and asynchronous `async def` in FastAPI?**
  - *Answer*: In FastAPI, an `async def` endpoint runs directly on the asyncio event loop and must use non-blocking `await` calls. If you declare a route as standard `def`, FastAPI automatically runs it in a separate external thread pool, preventing blocking operations from stalling the main event loop.
- **Q: How does FastAPI serialize Pydantic models to JSON?**
  - *Answer*: Pydantic v2 includes a compiled Rust core (`pydantic-core`) that directly serializes Python data structures into JSON strings (`model_dump_json()`), delivering 5x to 15x higher performance than standard Python json encoders.

### Database & Deduplication
- **Q: Why did you create an index on `normalized_url`?**
  - *Answer*: Without an index, checking whether a URL exists requires a full table scan ($O(N)$), which becomes increasingly slow as thousands of opportunities accumulate. A B-tree index enables logarithmic lookup time ($O(\log N)$).
- **Q: Why did you store `required_skills` as a JSON string in SQLite?**
  - *Answer*: SQLite does not support native array data types like PostgreSQL does. Storing skills as a JSON-serialized string (`'["Python", "React"]'`) allows us to store arbitrary lists of skills within a single column without needing a complex join table for simple local deployments.

### Agentic AI & Browser Automation
- **Q: What is the role of an Accessibility Tree in Browser Use?**
  - *Answer*: Raw HTML is bloated with thousands of non-functional tags, CSS styles, and tracking scripts that would overflow the LLM's context window. An Accessibility Tree represents only the semantic, interactive elements (buttons, inputs, headings) that screen readers use, allowing the LLM to reason over a compact, structured representation of the page.
- **Q: What is temperature in LLM generation, and what value did you use?**
  - *Answer*: Temperature controls the randomness of next-token sampling. For creative writing, high temperatures (0.8–1.0) are used; for structured entity extraction and agent actions, low temperatures (0.0–0.2) are required to ensure deterministic, schema-compliant outputs.

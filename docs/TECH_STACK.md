# Opportunity Hunter AI — Technology Stack Deep-Dive

This document details every technology, framework, library, and tool actually implemented in **Opportunity Hunter AI**.

---

## 1. React (v18.3)

1. **What is it?**: A declarative, component-based JavaScript library developed by Meta for building interactive user interfaces.
2. **Why chosen?**: To build a dynamic Single Page Application (SPA) where search progress, opportunity lists, bookmark states, and metrics update instantly without full-page browser reloads.
3. **What problem it solves**: Avoids manual, error-prone DOM manipulation (`document.getElementById`).
4. **How it works (simple terms)**: You describe what the UI should look like based on current data (State). When data changes, React calculates the minimal DOM changes needed using its Virtual DOM.
5. **Where used in codebase**: `frontend/src/App.jsx`, `frontend/src/pages/`, and `frontend/src/components/`.
6. **How it communicates**: Calls backend REST APIs over HTTP via `fetch()` in `frontend/src/services/api.js`.
7. **Alternatives & Trade-offs**: Vue.js, Svelte, or Angular. React was chosen for its vast ecosystem, industry standard adoption, and component modularity.
8. **Interviewer Question**: *"What is the difference between props and state in React?"*
   - *Answer*: Props are read-only configuration passed from parent to child; State is internal mutable data managed within the component that triggers re-renders when updated.

---

## 2. JavaScript (ES6+)

1. **What is it?**: The standard programming language of the modern web browser.
2. **Why chosen?**: Native execution in all web browsers; provides modern syntax (async/await, arrow functions, destructuring).
3. **What problem it solves**: Enables client-side interactivity, asynchronous network requests, and dynamic UI state.
4. **How it works**: Runs on the browser's V8 engine via a single-threaded event loop with non-blocking I/O.
5. **Where used in codebase**: All frontend files (`.jsx`, `.js`) and n8n Code nodes.
6. **How it communicates**: Powers React logic and interfaces with browser DOM APIs and Fetch API.
7. **Alternatives**: TypeScript. (TypeScript adds static types; we used standard modern JS for beginner accessibility, with Pydantic handling types on the backend).
8. **Interviewer Question**: *"How does the JavaScript event loop handle asynchronous tasks?"*
   - *Answer*: JavaScript runs synchronously on a single call stack. Asynchronous operations (like `fetch` or `setTimeout`) are offloaded to browser Web APIs; their callbacks wait in the Task Queue / Microtask Queue until the call stack is empty.

---

## 3. Tailwind CSS (v3.4)

1. **What is it?**: A utility-first CSS framework providing atomic class names.
2. **Why chosen?**: Allows rapid, consistent UI styling with dark navy typography, clean borders, and soft backgrounds without writing custom CSS files.
3. **What problem it solves**: Eliminates bloated custom CSS style sheets, naming collisions, and style drift.
4. **How it works**: You add utility classes directly in JSX (`className="flex p-4 rounded-2xl bg-white border border-slate-200"`). The compiler purges unused styles during build time.
5. **Where used in codebase**: `frontend/tailwind.config.js`, `frontend/src/index.css`, and throughout all JSX components.
6. **How it communicates**: Injected directly into the DOM styles by Vite.
7. **Alternatives**: Bootstrap, Styled Components, Material UI. Tailwind generates significantly smaller production bundles and offers total design control.
8. **Interviewer Question**: *"What are the benefits of utility-first CSS over traditional CSS stylesheets?"*
   - *Answer*: Zero context switching between CSS and markup, no CSS specificity conflicts, consistent design token enforcement, and automatic purging of unused CSS in production.

---

## 4. Vite (v5.4)

1. **What is it?**: A fast modern frontend build tool and development server created by Evan You.
2. **Why chosen?**: Provides near-instant server boot times (<200ms) and lightning-fast Hot Module Replacement (HMR).
3. **What problem it solves**: Traditional bundlers like Webpack re-bundle the entire application on every code save, causing multi-second delays.
4. **How it works**: Serves source code over native browser ES Modules during development; bundles with Rollup for optimized production output.
5. **Where used in codebase**: `frontend/vite.config.js` and `frontend/package.json`.
6. **How it communicates**: Acts as the local development web server and proxies `/api` calls to FastAPI on `http://127.0.0.1:8000`.
7. **Alternatives**: Create React App (deprecated), Webpack, Next.js. Vite is dramatically faster and avoids unnecessary SSR complexity for this dashboard.
8. **Interviewer Question**: *"Why does Vite start faster than Webpack in development?"*
   - *Answer*: Webpack crawls and bundles your entire codebase before starting; Vite divides code into dependencies (pre-bundled with esbuild) and source code (served on-demand via native browser ES Modules).

---

## 5. Python (v3.11 / v3.14)

1. **What is it?**: A high-level, dynamically typed programming language known for readability and an unmatched AI/ML ecosystem.
2. **Why chosen?**: The entire AI agent ecosystem (`browser-use`, `playwright`, `langchain`, `pydantic`, `fastapi`) is natively centered around Python.
3. **What problem it solves**: Provides first-class support for LLM libraries, asynchronous network programming, and data engineering.
4. **How it works**: Interpreted bytecode running on the CPython runtime.
5. **Where used in codebase**: All backend code in `backend/app/` and test suites in `backend/tests/`.
6. **How it communicates**: Runs the FastAPI ASGI server and controls Browser Use subprocesses.
7. **Alternatives**: Node.js/TypeScript, Go. While Node is great for web APIs, Python has vastly superior agentic AI library support.
8. **Interviewer Question**: *"What is the Global Interpreter Lock (GIL) in Python and does it affect this project?"*
   - *Answer*: The GIL allows only one thread to execute Python bytecode at a time. However, our backend relies heavily on `asyncio` and external I/O (browser automation, HTTP network calls, SQLite transactions), which release the GIL and do not bottleneck on CPU execution.

---

## 6. FastAPI (v0.142+)

1. **What is it?**: A modern, high-performance web framework for building APIs with Python based on standard type hints.
2. **Why chosen?**: Asynchronous performance, automatic Pydantic validation, and automatic OpenAPI (Swagger) documentation generation.
3. **What problem it solves**: Traditional frameworks like Flask are synchronous and require manual request validation boilerplate.
4. **How it works**: Uses `uvicorn` as an ASGI server. Inspects Python function type hints to parse and validate incoming JSON payloads.
5. **Where used in codebase**: `backend/app/main.py` and `backend/app/api/endpoints.py`.
6. **How it communicates**: Serves REST endpoints to React and receives webhook callbacks from n8n.
7. **Alternatives**: Flask, Django, Express.js. FastAPI is 3x faster than Flask and provides compile-time type validation via Pydantic.
8. **Interviewer Question**: *"How does FastAPI validate incoming request data?"*
   - *Answer*: It maps JSON request bodies into Pydantic models. If any field fails type or boundary constraints (e.g. `max_results > 50`), FastAPI halts execution and automatically returns an HTTP 422 error detailing the exact validation failure.

---

## 7. REST APIs & HTTP Protocol

1. **What is it?**: Architectural style for web communication using HTTP verbs: `GET`, `POST`, `PATCH`, `DELETE`.
2. **Why chosen?**: Standard, universally understood protocol between frontends, backends, and external automation tools.
3. **What problem it solves**: Provides a predictable contract for reading and manipulating resources.
4. **How it works**: Client sends request with Method, URL, Headers, and Body; server responds with Status Code and JSON payload.
5. **Where used in codebase**: Endpoints defined in `backend/app/api/endpoints.py`.
6. **How it communicates**: The standard language bridging React $\leftrightarrow$ FastAPI $\leftrightarrow$ n8n.
7. **Alternatives**: GraphQL, gRPC. REST is simpler, easier to cache, and natively supported by webhooks and n8n nodes.
8. **Interviewer Question**: *"What is the difference between POST and PATCH?"*
   - *Answer*: `POST` is typically used to create a new resource or trigger an action; `PATCH` is used to apply partial updates to an existing resource (e.g. updating an opportunity's status without re-sending the whole record).

---

## 8. SQLite (v3.50+)

1. **What is it?**: A self-contained, serverless, zero-configuration relational database engine.
2. **Why chosen?**: Stores all data in a single local file (`backend/data/opportunities.db`) with zero setup required by the user.
3. **What problem it solves**: Persists listings, execution logs, and preferences across server restarts without requiring a separate database server.
4. **How it works**: Compiles directly into the Python application process, storing structured tables with B-tree indexes.
5. **Where used in codebase**: `backend/app/database/db.py`.
6. **How it communicates**: Queried via Python's standard `sqlite3` module using parameterized SQL queries.
7. **Alternatives**: PostgreSQL, MySQL, MongoDB. SQLite is ideal for single-user local applications; PostgreSQL is the production path for multi-user concurrency.
8. **Interviewer Question**: *"What are the limitations of SQLite in a production environment?"*
   - *Answer*: SQLite uses database-level write locks. While it supports high-throughput concurrent reads, concurrent writes queue up and will throw 'database locked' errors under high multi-user traffic.

---

## 9. Browser Use Web AI (v0.13.10)

1. **What is it?**: An open-source agentic browser automation library that connects LLMs to web browsers.
2. **Why chosen?**: Purpose-built for autonomous web navigation, element perception, and structured data extraction.
3. **What problem it solves**: Traditional scrapers break on modern JavaScript SPAs and dynamic forms. Browser Use navigates websites like a human.
4. **How it works**: Builds an accessibility tree of interactive elements, provides that context to an LLM, and executes LLM-decided actions (click, type, scroll) in Playwright.
5. **Where used in codebase**: `backend/app/agents/browser_researcher.py`.
6. **How it communicates**: Interfaces with Playwright Chromium and calls LLMs via OpenRouter/OpenAI.
7. **Alternatives**: Selenium, Puppeteer, raw Playwright scripts. Browser Use adds cognitive reasoning and accessibility-tree pruning over raw script commands.
8. **Interviewer Question**: *"How does Browser Use prevent feeding massive HTML documents into the LLM?"*
   - *Answer*: It parses the DOM into an Accessibility Tree representation, filtering out non-interactive layout tags (`div`, `span`, CSS styling) and numbering only actionable elements (buttons, inputs, links).

---

## 10. Playwright (v1.63)

1. **What is it?**: Microsoft's browser automation framework for controlling Chromium, Firefox, and WebKit.
2. **Why chosen?**: Fast, reliable, supports modern Chromium features, and runs efficiently in headless mode.
3. **What problem it solves**: Executes real JavaScript in a genuine browser engine, rendering client-side React/Vue pages.
4. **How it works**: Communicates directly with Chromium over the Chrome DevTools Protocol (CDP) via asynchronous Python bindings.
5. **Where used in codebase**: Instantiated under the hood by `Browser(headless=True)` in `browser_researcher.py`.
6. **How it communicates**: Acts as the physical hands executing actions decided by Browser Use.
7. **Alternatives**: Selenium WebDriver. Playwright is much faster, auto-waits for elements to be actionable, and handles modern asynchronous web events natively.
8. **Interviewer Question**: *"What does headless browser mode mean?"*
   - *Answer*: Running the browser without a visual display window. It executes the exact same JavaScript engine and network stack but consumes substantially less RAM and CPU.

---

## 11. n8n Workflow Automation

1. **What is it?**: An extensible, open-source workflow automation platform with a visual node-based editor.
2. **Why chosen?**: Decouples scheduled cron harvesting, webhook listeners, and email dispatching from the core Python agent.
3. **What problem it solves**: Writing custom cron daemons, retry logic, and HTML email templates in pure Python creates maintenance complexity.
4. **How it works**: Executes event-driven pipelines where outputs from one node pass as structured JSON to downstream nodes.
5. **Where used in codebase**: `n8n/workflows/` (3 production workflow JSON files) and `n8n_client.py`.
6. **How it communicates**: Triggers FastAPI via HTTP requests and receives webhooks back.
7. **Alternatives**: Zapier, Make, Airflow, Temporal. n8n is self-hostable, open-source, and natively handles complex JSON payloads without per-task subscription fees.
8. **Interviewer Question**: *"Why use n8n instead of writing all workflows in Python?"*
   - *Answer*: Separation of concerns. n8n gives non-developers visual observability of running workflows, isolates scheduling and notification credentials, and allows changing email templates without redeploying backend code.

---

## 12. Large Language Models (LLMs) & OpenRouter

1. **What is it?**: Deep learning transformer models trained on massive corpora of code and text, capable of reasoning and structured data extraction.
2. **Why chosen?**: To evaluate unstructured job postings, filter out senior roles, identify implicit skill requirements, and format results into strict JSON schemas.
3. **What problem it solves**: No hardcoded regex can reliably parse every variation of job titles, deadlines, and requirements across the internet.
4. **How it works**: Receives page context and schema instructions; uses function calling or JSON mode to output typed fields.
5. **Where used in codebase**: Configured in `backend/app/agents/browser_researcher.py` using `ChatOpenRouter` or `ChatOpenAI`.
6. **How it communicates**: HTTP POST requests to API gateways (`https://openrouter.ai/api/v1`).
7. **Alternatives**: Self-hosted local models via Ollama or vLLM. OpenRouter was chosen because it allows switching between Llama 3.3, DeepSeek R1, and Claude with one configuration line.
8. **Interviewer Question**: *"How do you prevent the LLM from outputting conversational chatter instead of clean JSON?"*
   - *Answer*: By passing a Pydantic schema (`output_model_schema=OpportunityListOutput`), which instructs the model to use constrained decoding / function calling, guaranteeing valid JSON.

---

## 13. Uvicorn (v0.54)

1. **What is it?**: A lightning-fast ASGI (Asynchronous Server Gateway Interface) web server implementation for Python.
2. **Why chosen?**: The recommended production-grade server for running asynchronous FastAPI applications.
3. **What problem it solves**: Traditional WSGI servers (Gunicorn/uWSGI) are synchronous and block worker processes during long async I/O.
4. **How it works**: Built on top of `uvloop` (a fast C-based event loop implementation of `libuv`) and `httptools`.
5. **Where used in codebase**: Launched via `python3 -m uvicorn backend.app.main:app`.
6. **How it communicates**: Binds to `127.0.0.1:8000` and dispatches incoming TCP HTTP connections to FastAPI routes.
7. **Alternatives**: Hypercorn, Daphne. Uvicorn is the benchmark performance leader for Python ASGI.
8. **Interviewer Question**: *"What is the difference between Uvicorn and Gunicorn?"*
   - *Answer*: Uvicorn is an ASGI web server that runs the async event loop; Gunicorn is a process manager. In large production deployments, you run Gunicorn as a process manager with Uvicorn worker classes (`gunicorn -k uvicorn.workers.UvicornWorker`).

---

## 14. Environment Variables & API Key Security

1. **What is it?**: Configuration values injected into the operating system process at runtime, rather than hardcoded in source code files.
2. **Why chosen?**: Enforces security best practices by keeping secret keys (`OPENROUTER_API_KEY`, `N8N_API_KEY`) out of Git.
3. **What problem it solves**: Prevents accidental leakage of paid API keys on public GitHub repositories.
4. **How it works**: Values in `backend/.env` are parsed on boot by `python-dotenv` into `os.environ`.
5. **Where used in codebase**: `backend/.env`, `backend/.env.example`, and loaded in `backend/app/main.py`.
6. **How it communicates**: Read by backend services via `os.getenv("VARIABLE_NAME")`.
7. **Alternatives**: HashiCorp Vault, AWS Secrets Manager. For local full-stack development, `.env` files are the universal standard.
8. **Interviewer Question**: *"Why must API keys never be prefixed with VITE_ on the frontend?"*
   - *Answer*: Any variable with a `VITE_` prefix is automatically embedded into the public static JavaScript files during compilation, meaning any user can open Chrome DevTools and steal your secret API key.

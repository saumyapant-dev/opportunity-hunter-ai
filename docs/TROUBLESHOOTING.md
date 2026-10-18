# Opportunity Hunter AI — Troubleshooting & Debugging Manual

A comprehensive engineering guide for diagnosing and fixing common local development, network, and runtime issues.

---

## Quick Reference Table

| Symptom / Error | Root Cause | Immediate Fix |
|---|---|---|
| `[Errno 48] address already in use` | Old process occupying port 8000 or 5173 | Kill stale process via `kill -9 $(lsof -t -i:8000)` |
| `PermissionError: /Users/.../.config/browseruse` | Restricted OS permissions in home directory | Set `BROWSER_USE_CONFIG_DIR=./.browseruse` |
| `openai.AuthenticationError: 401 Invalid API Key` | Missing or invalid key in `backend/.env` | Update `OPENROUTER_API_KEY` or switch to `LLM_PROVIDER=mock` |
| `Executable doesn't exist at ms-playwright/...` | Playwright Chromium binaries not downloaded | Run `python3 -m playwright install chromium` |
| `sqlite3.OperationalError: database is locked` | Concurrent write lock in SQLite | Add `timeout=10.0` in `get_db_connection()` |
| `Access-Control-Allow-Origin blocked by CORS` | Missing frontend origin in backend CORS config | Update `CORS_ORIGINS` in `backend/.env` |
| `Could not connect to n8n webhook at port 5678` | n8n is not running or workflow is inactive | Start n8n via `npx n8n` and toggle workflow to Active |

---

## 1. Port Conflicts (Address Already in Use)

### Symptom
```
ERROR:    [Errno 48] error while attempting to bind on address ('127.0.0.1', 8000): address already in use
```
or Vite dev server fails to bind to `http://localhost:5173`.

### Why It Happens
A previous instance of Uvicorn or Vite was terminated improperly or is still running in the background.

### Step-by-Step Fix
1. Inspect which process is occupying the port:
   ```bash
   lsof -i :8000
   lsof -i :5173
   ```
2. Terminate the process:
   ```bash
   kill -9 $(lsof -t -i:8000)
   kill -9 $(lsof -t -i:5173)
   ```
3. Restart the server.

---

## 2. Browser Use Permission Error (`~/.config/browseruse`)

### Symptom
```
PermissionError: [Errno 1] Operation not permitted: '/Users/saumyapant/.config/browseruse'
```

### Why It Happens
By default, the `browser-use` library attempts to create a directory in `~/.config/browseruse` to store profile data. In sandboxed environments or macOS systems with restricted directory write permissions, this raises an OS `PermissionError`.

### Step-by-Step Fix
In Opportunity Hunter AI, this is handled automatically in `backend/app/main.py` and `browser_researcher.py` by routing configuration paths via an environment variable. If you ever encounter it outside the app, ensure `BROWSER_USE_CONFIG_DIR` points to a project-local directory:
```bash
export BROWSER_USE_CONFIG_DIR="/Users/saumyapant/Desktop/opp hunter/.browseruse"
```

---

## 3. LLM API Key Errors & Quota Limits

### Symptom
```
openai.AuthenticationError: Error code: 401 - {'error': {'message': 'Invalid API Key'}}
```
or `RateLimitError: 429 - Insufficient quota`.

### Why It Happens
The API key provided in `backend/.env` is invalid, expired, or has run out of credits.

### Step-by-Step Fix
- **Zero-Cost Immediate Fix**: Set `LLM_PROVIDER=mock` in `backend/.env`. The application will instantly switch to the high-fidelity mock engine without requiring any paid tokens.
- **For Live AI**: Obtain a valid key from [OpenRouter](https://openrouter.ai/keys) or OpenAI, paste it into `backend/.env` under `OPENROUTER_API_KEY`, and set `LLM_PROVIDER=openrouter`.

---

## 4. Playwright Chromium Missing Binaries

### Symptom
```
playwright._impl._errors.Error: Executable doesn't exist at /Users/.../ms-playwright/chromium-...
```

### Why It Happens
The `playwright` Python library is installed, but its native Chromium browser binaries have not been downloaded.

### Step-by-Step Fix
Run Playwright's automated browser installer in your terminal:
```bash
python3 -m playwright install chromium
```

---

## 5. SQLite Database Locked Error

### Symptom
```
sqlite3.OperationalError: database is locked
```

### Why It Happens
SQLite locks the entire database file during write transactions. If multiple threads write simultaneously, collisions occur.

### Step-by-Step Fix
1. In `backend/app/database/db.py`, ensure all database connections close promptly.
2. Add a busy-timeout to SQLite connection initialization:
   ```python
   conn = sqlite3.connect(str(path), timeout=10.0)
   ```
3. For multi-user production deployments, migrate to PostgreSQL (see `docs/ARCHITECTURE.md`).

---

## 6. CORS (Cross-Origin Resource Sharing) Error

### Symptom
```
Access to fetch at 'http://127.0.0.1:8000/api/opportunities' from origin 'http://localhost:5173'
has been blocked by CORS policy.
```

### Why It Happens
The browser blocks requests because the origin host header does not match the backend's allowed origins list.

### Step-by-Step Fix
In `backend/.env`, ensure both `localhost` and `127.0.0.1` are present in `CORS_ORIGINS`:
```ini
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```
Restart the FastAPI backend.

---

## 7. n8n Webhook Connection Refused

### Symptom
```
Could not connect to n8n webhook at http://localhost:5678/webhook/opportunity-research. Is n8n running?
```

### Why It Happens
The backend attempted to dispatch a research payload to n8n, but n8n is not running on port 5678, or the workflow has not been set to **Active**.

### How the System Protects You
FastAPI automatically catches this error, logs a warning, and **falls back to the internal direct background runner**, ensuring the user's search still succeeds.

### Step-by-Step Fix
1. Start n8n in a terminal:
   ```bash
   npx n8n
   ```
2. Open `http://localhost:5678`, open `Opportunity Hunter - Manual Discovery`, and ensure the switch in the top right is toggled from **Inactive** to **Active**.

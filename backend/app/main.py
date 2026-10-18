"""Main FastAPI application entrypoint for Opportunity Hunter AI."""
import os
import logging
from contextlib import asynccontextmanager
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
backend_dir = Path(__file__).resolve().parent.parent
load_dotenv(backend_dir / ".env")

# Ensure .browseruse dir is configured
project_root = backend_dir.parent
default_config_dir = project_root / ".browseruse"
default_config_dir.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("BROWSER_USE_CONFIG_DIR", str(default_config_dir))

from .database.db import init_db
from .api.endpoints import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("opportunity_hunter")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle manager for database bootstrap."""
    logger.info("Initializing Opportunity Hunter SQLite database...")
    init_db()
    logger.info("Database initialized successfully.")
    yield
    logger.info("Opportunity Hunter backend shutting down.")


app = FastAPI(
    title="Opportunity Hunter AI API",
    description="Intelligent student opportunity discovery agent platform with Browser Use and n8n orchestration.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS configuration for local React frontend
cors_origins_env = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
origins = [origin.strip() for origin in cors_origins_env.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import HTTPException

# Mount API endpoints
app.include_router(router)

# Production Static Files & SPA Routing Fallback
frontend_dist = project_root / "frontend" / "dist"
if frontend_dist.exists():
    assets_dir = frontend_dist / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_frontend(full_path: str):
        # Do not intercept API, health, or OpenAPI documentation endpoints
        if full_path.startswith(("api/", "health", "docs", "openapi.json", "redoc")):
            raise HTTPException(status_code=404, detail="Endpoint not found")

        candidate_file = frontend_dist / full_path
        if full_path and candidate_file.is_file():
            return FileResponse(candidate_file)
        
        index_file = frontend_dist / "index.html"
        if index_file.is_file():
            return FileResponse(index_file)
        raise HTTPException(status_code=404, detail="Frontend build index.html not found")


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("ENVIRONMENT", "development").lower() == "development"
    uvicorn.run("backend.app.main:app", host=host, port=port, reload=reload)

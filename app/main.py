"""Application entrypoint for the SmartCV Analyzer API."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import api_router
from app.core.config import API_V1_PREFIX, APP_TITLE, APP_VERSION

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

app = FastAPI(
    title=APP_TITLE,
    version=APP_VERSION,
)

app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")
app.include_router(api_router, prefix=API_V1_PREFIX)


@app.get("/", include_in_schema=False)
def serve_frontend() -> FileResponse:
    """Serve the static frontend entrypoint."""
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    """Return the API health status."""
    return {"status": "ok"}

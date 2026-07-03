"""Application entrypoint for the SmartCV Analyzer API."""

from fastapi import FastAPI

from app.api.routes import api_router
from app.core.config import API_V1_PREFIX, APP_TITLE, APP_VERSION

app = FastAPI(
    title=APP_TITLE,
    version=APP_VERSION,
)

app.include_router(api_router, prefix=API_V1_PREFIX)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    """Return the API health status."""
    return {"status": "ok"}

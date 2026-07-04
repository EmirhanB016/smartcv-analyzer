"""Application configuration values."""

import os


def _env_bool(name: str, default: bool) -> bool:
    raw_value = os.getenv(name)
    if raw_value is None:
        return default

    return raw_value.strip().casefold() not in {"0", "false", "no", "off"}


APP_TITLE = "SmartCV Analyzer"
APP_VERSION = "0.1.0"
API_V1_PREFIX = "/api/v1"
SMARTCV_EMBEDDINGS_ENABLED = _env_bool("SMARTCV_EMBEDDINGS_ENABLED", default=True)

MAX_CV_FILE_SIZE_BYTES = 5 * 1024 * 1024
SUPPORTED_CV_EXTENSIONS = {".pdf", ".docx"}

GENERIC_CONTENT_TYPES = {
    "",
    "application/octet-stream",
    "binary/octet-stream",
}

SUPPORTED_CV_CONTENT_TYPES = {
    ".pdf": {"application/pdf"},
    ".docx": {
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/zip",
    },
}


def embeddings_enabled() -> bool:
    """Return whether heavyweight sentence-transformers embeddings should run."""
    return _env_bool(
        "SMARTCV_EMBEDDINGS_ENABLED",
        default=SMARTCV_EMBEDDINGS_ENABLED,
    )

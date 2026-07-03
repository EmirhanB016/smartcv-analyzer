"""Application configuration values."""

APP_TITLE = "SmartCV Analyzer"
APP_VERSION = "0.1.0"
API_V1_PREFIX = "/api/v1"

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

"""Error response schemas and documented API error codes."""

from enum import Enum
from typing import NoReturn

from fastapi import HTTPException, status
from pydantic import BaseModel


class ErrorCode(str, Enum):
    """Documented API error codes."""

    MISSING_FILE = "MISSING_FILE"
    EMPTY_JOB_DESCRIPTION = "EMPTY_JOB_DESCRIPTION"
    UNSUPPORTED_FILE_TYPE = "UNSUPPORTED_FILE_TYPE"
    FILE_TOO_LARGE = "FILE_TOO_LARGE"
    TEXT_EXTRACTION_FAILED = "TEXT_EXTRACTION_FAILED"
    ANALYSIS_FAILED = "ANALYSIS_FAILED"


class ErrorDetail(BaseModel):
    """Error payload returned inside the FastAPI `detail` field."""

    code: ErrorCode
    message: str


class ErrorResponse(BaseModel):
    """Standard error response shape."""

    detail: ErrorDetail


ERROR_MESSAGES = {
    ErrorCode.MISSING_FILE: "CV file is required.",
    ErrorCode.EMPTY_JOB_DESCRIPTION: "Job description must not be empty.",
    ErrorCode.UNSUPPORTED_FILE_TYPE: "Only PDF and DOCX files are supported.",
    ErrorCode.FILE_TOO_LARGE: "The uploaded file exceeds the 5 MB size limit.",
    ErrorCode.TEXT_EXTRACTION_FAILED: "Could not extract readable text from the uploaded CV.",
    ErrorCode.ANALYSIS_FAILED: "An unexpected error occurred during analysis.",
}

ERROR_STATUS_CODES = {
    ErrorCode.MISSING_FILE: status.HTTP_400_BAD_REQUEST,
    ErrorCode.EMPTY_JOB_DESCRIPTION: status.HTTP_400_BAD_REQUEST,
    ErrorCode.UNSUPPORTED_FILE_TYPE: status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    ErrorCode.FILE_TOO_LARGE: status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
    ErrorCode.TEXT_EXTRACTION_FAILED: status.HTTP_422_UNPROCESSABLE_ENTITY,
    ErrorCode.ANALYSIS_FAILED: status.HTTP_500_INTERNAL_SERVER_ERROR,
}


def raise_api_error(code: ErrorCode) -> NoReturn:
    """Raise an HTTPException with the documented error payload."""
    raise HTTPException(
        status_code=ERROR_STATUS_CODES[code],
        detail={
            "code": code.value,
            "message": ERROR_MESSAGES[code],
        },
    )

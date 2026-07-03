"""Validation helpers for uploaded CV files and job descriptions."""

from dataclasses import dataclass
from pathlib import PurePath

from fastapi import UploadFile

from app.core.config import (
    GENERIC_CONTENT_TYPES,
    MAX_CV_FILE_SIZE_BYTES,
    SUPPORTED_CV_CONTENT_TYPES,
    SUPPORTED_CV_EXTENSIONS,
)
from app.schemas.errors import ErrorCode, raise_api_error


@dataclass(frozen=True)
class ValidatedCVFile:
    """Validated in-memory CV upload data."""

    filename: str
    extension: str
    content: bytes
    content_type: str | None = None


def validate_job_description(job_description: str | None) -> str:
    """Validate and normalize the required job description input."""
    if job_description is None or not job_description.strip():
        raise_api_error(ErrorCode.EMPTY_JOB_DESCRIPTION)

    return job_description.strip()


async def validate_upload_file(cv_file: UploadFile | None) -> ValidatedCVFile:
    """Read and validate a FastAPI UploadFile without persisting it."""
    if cv_file is None:
        raise_api_error(ErrorCode.MISSING_FILE)

    content = await cv_file.read(MAX_CV_FILE_SIZE_BYTES + 1)
    await cv_file.seek(0)

    return validate_cv_file(
        filename=cv_file.filename,
        content=content,
        content_type=cv_file.content_type,
    )


def validate_cv_file(
    filename: str | None,
    content: bytes | None,
    content_type: str | None = None,
) -> ValidatedCVFile:
    """Validate an uploaded CV file that has already been read into memory."""
    if not filename or content is None:
        raise_api_error(ErrorCode.MISSING_FILE)

    extension = PurePath(filename).suffix.lower()
    if extension not in SUPPORTED_CV_EXTENSIONS:
        raise_api_error(ErrorCode.UNSUPPORTED_FILE_TYPE)

    if len(content) > MAX_CV_FILE_SIZE_BYTES:
        raise_api_error(ErrorCode.FILE_TOO_LARGE)

    validate_content_type(extension, content_type)

    return ValidatedCVFile(
        filename=filename,
        extension=extension,
        content=content,
        content_type=content_type,
    )


def validate_content_type(extension: str, content_type: str | None) -> None:
    """Reject clearly incompatible content types when the client provides one."""
    if content_type is None:
        return

    normalized_content_type = content_type.split(";", maxsplit=1)[0].strip().lower()
    if normalized_content_type in GENERIC_CONTENT_TYPES:
        return

    supported_content_types = SUPPORTED_CV_CONTENT_TYPES.get(extension, set())
    if normalized_content_type not in supported_content_types:
        raise_api_error(ErrorCode.UNSUPPORTED_FILE_TYPE)

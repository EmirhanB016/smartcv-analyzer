from fastapi import HTTPException
import pytest

from app.core.config import MAX_CV_FILE_SIZE_BYTES
from app.utils.validators import validate_cv_file, validate_job_description


def test_validate_cv_file_accepts_supported_pdf_and_docx_extensions() -> None:
    pdf_file = validate_cv_file("cv.pdf", b"pdf content", "application/pdf")
    docx_file = validate_cv_file(
        "cv.docx",
        b"docx content",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

    assert pdf_file.extension == ".pdf"
    assert docx_file.extension == ".docx"


def test_validate_cv_file_accepts_generic_content_type_when_extension_is_supported() -> None:
    cv_file = validate_cv_file("cv.pdf", b"pdf content", "application/octet-stream")

    assert cv_file.content_type == "application/octet-stream"


def test_validate_cv_file_rejects_unsupported_extension() -> None:
    with pytest.raises(HTTPException) as exc_info:
        validate_cv_file("cv.txt", b"text content", "text/plain")

    assert exc_info.value.status_code == 415
    assert exc_info.value.detail["code"] == "UNSUPPORTED_FILE_TYPE"


def test_validate_cv_file_rejects_incompatible_content_type() -> None:
    with pytest.raises(HTTPException) as exc_info:
        validate_cv_file("cv.pdf", b"pdf content", "text/plain")

    assert exc_info.value.status_code == 415
    assert exc_info.value.detail["code"] == "UNSUPPORTED_FILE_TYPE"


def test_validate_cv_file_rejects_oversized_file() -> None:
    with pytest.raises(HTTPException) as exc_info:
        validate_cv_file("cv.pdf", b"x" * (MAX_CV_FILE_SIZE_BYTES + 1), "application/pdf")

    assert exc_info.value.status_code == 413
    assert exc_info.value.detail["code"] == "FILE_TOO_LARGE"


def test_validate_cv_file_requires_filename_and_content() -> None:
    with pytest.raises(HTTPException) as exc_info:
        validate_cv_file(None, b"content")

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail["code"] == "MISSING_FILE"

    with pytest.raises(HTTPException) as exc_info:
        validate_cv_file("cv.pdf", None)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail["code"] == "MISSING_FILE"


def test_validate_job_description_trims_and_rejects_empty_text() -> None:
    assert validate_job_description("  Python developer  ") == "Python developer"

    with pytest.raises(HTTPException) as exc_info:
        validate_job_description("   ")

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail["code"] == "EMPTY_JOB_DESCRIPTION"

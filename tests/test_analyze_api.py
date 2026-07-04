from io import BytesIO

import fitz
from docx import Document
from fastapi.testclient import TestClient

from app.core.config import MAX_CV_FILE_SIZE_BYTES
from app.main import app

client = TestClient(app)


CV_TEXT = """
Jane Developer
jane@example.com

Professional summary
Backend developer building REST API services with Python and FastAPI.

Skills
Python, FastAPI, Docker, SQL, REST API, Git

Work experience
Built API integrations and database-backed services for product teams.

Education
Computer Engineering

Projects
SmartCV Analyzer - Python FastAPI project with Docker and SQL support.

Certifications
Cloud fundamentals
"""

JOB_DESCRIPTION = (
    "We are looking for a Python developer with FastAPI, Docker, SQL, "
    "REST API, Git, and backend development experience."
)


def test_health_endpoint_still_works() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analyze_accepts_valid_docx(monkeypatch) -> None:
    monkeypatch.setattr("app.api.routes.calculate_semantic_similarity", lambda *_: 0.82)

    response = client.post(
        "/api/v1/analyze",
        files={
            "cv_file": (
                "cv.docx",
                _build_docx_bytes(CV_TEXT),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        },
        data={"job_description": JOB_DESCRIPTION},
    )

    payload = response.json()
    assert response.status_code == 200
    assert set(payload) == {
        "overall_score",
        "semantic_similarity",
        "matched_keywords",
        "missing_keywords",
        "section_analysis",
        "suggestions",
        "extracted_cv_text_preview",
    }
    assert 0 <= payload["overall_score"] <= 100
    assert payload["semantic_similarity"] == 0.82
    assert 0 <= payload["semantic_similarity"] <= 1
    assert "Python" in payload["matched_keywords"]
    assert payload["section_analysis"]
    assert payload["suggestions"]
    assert any("CV'niz" in suggestion for suggestion in payload["suggestions"])
    assert "FastAPI" in payload["extracted_cv_text_preview"]


def test_analyze_accepts_valid_pdf(monkeypatch) -> None:
    monkeypatch.setattr("app.api.routes.calculate_semantic_similarity", lambda *_: 0.76)

    response = client.post(
        "/api/v1/analyze",
        files={"cv_file": ("cv.pdf", _build_pdf_bytes(CV_TEXT), "application/pdf")},
        data={"job_description": JOB_DESCRIPTION},
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload["semantic_similarity"] == 0.76
    assert 0 <= payload["overall_score"] <= 100
    assert 0 <= payload["semantic_similarity"] <= 1
    assert isinstance(payload["matched_keywords"], list)
    assert isinstance(payload["missing_keywords"], list)


def test_analyze_returns_required_fields_when_embeddings_are_disabled(monkeypatch) -> None:
    monkeypatch.setenv("SMARTCV_EMBEDDINGS_ENABLED", "false")

    response = client.post(
        "/api/v1/analyze",
        files={
            "cv_file": (
                "cv.docx",
                _build_docx_bytes(CV_TEXT),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        },
        data={"job_description": JOB_DESCRIPTION},
    )

    payload = response.json()
    assert response.status_code == 200
    assert set(payload) == {
        "overall_score",
        "semantic_similarity",
        "matched_keywords",
        "missing_keywords",
        "section_analysis",
        "suggestions",
        "extracted_cv_text_preview",
    }
    assert 0 <= payload["overall_score"] <= 100
    assert 0 <= payload["semantic_similarity"] <= 1
    assert isinstance(payload["matched_keywords"], list)
    assert isinstance(payload["missing_keywords"], list)
    assert payload["section_analysis"]
    assert payload["suggestions"]


def test_analyze_missing_file_returns_documented_error() -> None:
    response = client.post(
        "/api/v1/analyze",
        data={"job_description": JOB_DESCRIPTION},
    )

    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "MISSING_FILE"


def test_analyze_empty_job_description_returns_documented_error() -> None:
    response = client.post(
        "/api/v1/analyze",
        files={
            "cv_file": (
                "cv.docx",
                _build_docx_bytes(CV_TEXT),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        },
        data={"job_description": "   "},
    )

    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "EMPTY_JOB_DESCRIPTION"


def test_analyze_unsupported_file_type_returns_documented_error() -> None:
    response = client.post(
        "/api/v1/analyze",
        files={"cv_file": ("cv.txt", b"plain text", "text/plain")},
        data={"job_description": JOB_DESCRIPTION},
    )

    assert response.status_code == 415
    assert response.json()["detail"]["code"] == "UNSUPPORTED_FILE_TYPE"


def test_analyze_oversized_file_returns_documented_error() -> None:
    response = client.post(
        "/api/v1/analyze",
        files={
            "cv_file": (
                "large.pdf",
                b"x" * (MAX_CV_FILE_SIZE_BYTES + 1),
                "application/pdf",
            )
        },
        data={"job_description": JOB_DESCRIPTION},
    )

    assert response.status_code == 413
    assert response.json()["detail"]["code"] == "FILE_TOO_LARGE"


def test_analyze_unreadable_file_returns_documented_error() -> None:
    response = client.post(
        "/api/v1/analyze",
        files={"cv_file": ("broken.pdf", b"not a real pdf", "application/pdf")},
        data={"job_description": JOB_DESCRIPTION},
    )

    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "TEXT_EXTRACTION_FAILED"


def test_analyze_unexpected_errors_return_documented_error(monkeypatch) -> None:
    def fail_keyword_extraction(*_) -> list[str]:
        raise RuntimeError("boom")

    monkeypatch.setattr("app.api.routes.extract_keywords", fail_keyword_extraction)

    response = client.post(
        "/api/v1/analyze",
        files={
            "cv_file": (
                "cv.docx",
                _build_docx_bytes(CV_TEXT),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        },
        data={"job_description": JOB_DESCRIPTION},
    )

    assert response.status_code == 500
    assert response.json()["detail"]["code"] == "ANALYSIS_FAILED"


def _build_docx_bytes(text: str) -> bytes:
    document = Document()
    for paragraph in text.strip().split("\n\n"):
        document.add_paragraph(paragraph.strip())

    stream = BytesIO()
    document.save(stream)
    return stream.getvalue()


def _build_pdf_bytes(text: str) -> bytes:
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), text.strip(), fontsize=10)
    content = document.tobytes()
    document.close()
    return content

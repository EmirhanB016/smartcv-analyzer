"""Versioned API routes for SmartCV Analyzer."""

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.schemas.analysis import AnalysisResponse, SectionAnalysisItem
from app.schemas.errors import ErrorCode, ErrorResponse, raise_api_error
from app.services.embedding_service import calculate_semantic_similarity
from app.services.feedback_service import generate_suggestions
from app.services.file_extraction_service import extract_cv_text
from app.services.keyword_service import extract_keywords, match_keywords
from app.services.scoring_service import (
    calculate_keyword_match_ratio,
    calculate_overall_score,
    calculate_section_score,
)
from app.services.section_detection import SECTION_ORDER
from app.services.section_detection_service import detect_sections
from app.utils.text_cleaning import clean_text
from app.utils.validators import validate_job_description, validate_upload_file

api_router = APIRouter()

TEXT_PREVIEW_LIMIT = 800

SECTION_DISPLAY_NAMES = {
    "contact": "Contact information",
    "summary": "Professional summary",
    "skills": "Skills",
    "experience": "Work experience",
    "education": "Education",
    "projects": "Projects",
    "certifications": "Certifications",
}

ANALYZE_ERROR_RESPONSES = {
    400: {"model": ErrorResponse},
    413: {"model": ErrorResponse},
    415: {"model": ErrorResponse},
    422: {"model": ErrorResponse},
    500: {"model": ErrorResponse},
}


@api_router.post(
    "/analyze",
    response_model=AnalysisResponse,
    responses=ANALYZE_ERROR_RESPONSES,
    tags=["Analysis"],
)
async def analyze_cv(
    cv_file: UploadFile | None = File(default=None),
    job_description: str | None = Form(default=None),
) -> AnalysisResponse:
    """Analyze one uploaded CV against one pasted job description."""
    try:
        validated_file = await validate_upload_file(cv_file)
        validated_job_description = validate_job_description(job_description)

        extracted_cv_text = extract_cv_text(validated_file)
        cleaned_cv_text = clean_text(extracted_cv_text)
        cleaned_job_description = clean_text(validated_job_description)

        keywords = extract_keywords(cleaned_job_description)
        keyword_matches = match_keywords(cleaned_cv_text, keywords)
        matched_keywords = keyword_matches["matched_keywords"]
        missing_keywords = keyword_matches["missing_keywords"]

        section_analysis = detect_sections(cleaned_cv_text)
        semantic_similarity = round(
            calculate_semantic_similarity(cleaned_cv_text, cleaned_job_description),
            4,
        )
        keyword_match_ratio = calculate_keyword_match_ratio(matched_keywords, keywords)
        section_score = calculate_section_score(section_analysis)
        overall_score = calculate_overall_score(
            semantic_similarity=semantic_similarity,
            keyword_match_ratio=keyword_match_ratio,
            section_score=section_score,
        )
        suggestions = generate_suggestions(
            overall_score=overall_score,
            matched_keywords=matched_keywords,
            missing_keywords=missing_keywords,
            section_analysis=section_analysis,
            semantic_similarity=semantic_similarity,
        )

        return AnalysisResponse(
            overall_score=overall_score,
            semantic_similarity=semantic_similarity,
            matched_keywords=matched_keywords,
            missing_keywords=missing_keywords,
            section_analysis=_format_section_analysis(section_analysis),
            suggestions=suggestions,
            extracted_cv_text_preview=_build_text_preview(cleaned_cv_text),
        )
    except HTTPException:
        raise
    except Exception:
        raise_api_error(ErrorCode.ANALYSIS_FAILED)


def _format_section_analysis(
    section_analysis: dict[str, dict[str, str]],
) -> list[SectionAnalysisItem]:
    return [
        SectionAnalysisItem(
            section=SECTION_DISPLAY_NAMES.get(section_name, section_name.title()),
            status=section_analysis[section_name]["status"],
            message=section_analysis[section_name]["message"],
        )
        for section_name in SECTION_ORDER
        if section_name in section_analysis
    ]


def _build_text_preview(cv_text: str) -> str:
    if len(cv_text) <= TEXT_PREVIEW_LIMIT:
        return cv_text

    return f"{cv_text[:TEXT_PREVIEW_LIMIT].rstrip()}..."

"""Analysis request and response schemas."""

from typing import Literal

from pydantic import BaseModel

SectionStatus = Literal["present", "weak", "missing"]


class SectionAnalysisItem(BaseModel):
    """Section status and user-facing Turkish message."""

    section: str
    status: SectionStatus
    message: str


class AnalysisResponse(BaseModel):
    """Full CV analysis response returned by the analyze endpoint."""

    overall_score: int
    semantic_similarity: float
    matched_keywords: list[str]
    missing_keywords: list[str]
    section_analysis: list[SectionAnalysisItem]
    suggestions: list[str]
    extracted_cv_text_preview: str


class FeedbackResult(BaseModel):
    """Deterministic Turkish feedback output."""

    summary: str
    suggestions: list[str]

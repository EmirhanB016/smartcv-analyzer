"""Compatibility wrapper for deterministic feedback generation functions."""

from app.services.feedback import (
    generate_keyword_suggestion,
    generate_score_summary,
    generate_section_suggestions,
    generate_suggestions,
    get_score_category,
)

__all__ = [
    "generate_keyword_suggestion",
    "generate_score_summary",
    "generate_section_suggestions",
    "generate_suggestions",
    "get_score_category",
]

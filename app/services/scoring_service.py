"""Compatibility wrapper for scoring service functions."""

from app.services.scoring import (
    SECTION_STATUS_VALUES,
    calculate_keyword_match_ratio,
    calculate_overall_score,
    calculate_section_score,
)

__all__ = [
    "SECTION_STATUS_VALUES",
    "calculate_keyword_match_ratio",
    "calculate_overall_score",
    "calculate_section_score",
]

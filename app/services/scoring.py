"""Compatibility scoring helpers."""

from collections.abc import Mapping, Sequence
from typing import Any

from app.services.section_detection import SECTION_ORDER

SECTION_STATUS_VALUES = {
    "present": 1.0,
    "weak": 0.5,
    "missing": 0.0,
}


def calculate_keyword_match_ratio(
    matched_keywords: Sequence[str],
    total_keywords: Sequence[str] | int,
) -> float:
    """Calculate matched keyword count divided by extracted keyword count."""
    total_keyword_count = (
        total_keywords if isinstance(total_keywords, int) else len(total_keywords)
    )
    if total_keyword_count <= 0:
        return 0.0

    ratio = len(matched_keywords) / total_keyword_count
    return _clamp_float(ratio, 0.0, 1.0)


def calculate_section_score(section_analysis: Mapping[str, Any] | Sequence[Any]) -> float:
    """Average supported section statuses using present/weak/missing values."""
    normalized_sections = _normalize_section_analysis(section_analysis)
    if not normalized_sections:
        return 0.0

    scores = [
        SECTION_STATUS_VALUES.get(normalized_sections.get(section, "missing"), 0.0)
        for section in SECTION_ORDER
    ]
    return _clamp_float(sum(scores) / len(scores), 0.0, 1.0)


def calculate_overall_score(
    semantic_similarity: float,
    keyword_match_ratio: float,
    section_score: float,
) -> int:
    """Calculate the weighted final score and clamp it to 0..100."""
    semantic_similarity = _clamp_float(semantic_similarity, 0.0, 1.0)
    keyword_match_ratio = _clamp_float(keyword_match_ratio, 0.0, 1.0)
    section_score = _clamp_float(section_score, 0.0, 1.0)

    overall_score = round(
        (
            semantic_similarity * 0.50
            + keyword_match_ratio * 0.30
            + section_score * 0.20
        )
        * 100
    )
    return int(_clamp_float(overall_score, 0, 100))


def _normalize_section_analysis(
    section_analysis: Mapping[str, Any] | Sequence[Any],
) -> dict[str, str]:
    if isinstance(section_analysis, Mapping):
        return {
            str(section).casefold(): _extract_status(value)
            for section, value in section_analysis.items()
        }

    normalized_sections: dict[str, str] = {}
    for item in section_analysis:
        if isinstance(item, Mapping):
            section = item.get("section")
            status = item.get("status")
        else:
            section = getattr(item, "section", None)
            status = getattr(item, "status", None)

        if section is not None:
            normalized_sections[str(section).casefold()] = _normalize_status(status)

    return normalized_sections


def _extract_status(value: Any) -> str:
    if isinstance(value, Mapping):
        return _normalize_status(value.get("status"))
    return _normalize_status(value)


def _normalize_status(status: Any) -> str:
    normalized_status = str(status or "").casefold()
    if normalized_status in SECTION_STATUS_VALUES:
        return normalized_status
    return "missing"


def _clamp_float(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, float(value)))

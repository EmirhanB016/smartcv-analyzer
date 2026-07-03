import pytest

from app.services.scoring import (
    calculate_keyword_match_ratio,
    calculate_overall_score,
    calculate_section_score,
)


def test_calculate_keyword_match_ratio() -> None:
    assert calculate_keyword_match_ratio(["Python", "FastAPI"], ["Python", "FastAPI", "Docker"]) == pytest.approx(2 / 3)
    assert calculate_keyword_match_ratio(["Python"], 4) == pytest.approx(0.25)


def test_calculate_keyword_match_ratio_returns_zero_when_no_keywords_exist() -> None:
    assert calculate_keyword_match_ratio(["Python"], []) == 0.0
    assert calculate_keyword_match_ratio([], 0) == 0.0


def test_calculate_keyword_match_ratio_is_clamped() -> None:
    assert calculate_keyword_match_ratio(["Python", "FastAPI", "Docker"], 2) == 1.0


def test_calculate_section_score_averages_all_supported_sections() -> None:
    section_analysis = {
        "contact": {"status": "present"},
        "summary": {"status": "weak"},
        "skills": {"status": "missing"},
        "experience": {"status": "present"},
        "education": {"status": "weak"},
        "projects": {"status": "missing"},
        "certifications": {"status": "present"},
    }

    assert calculate_section_score(section_analysis) == pytest.approx(4 / 7)


def test_calculate_section_score_treats_absent_supported_sections_as_missing() -> None:
    assert calculate_section_score({"contact": {"status": "present"}}) == pytest.approx(1 / 7)


def test_calculate_section_score_accepts_status_strings() -> None:
    assert calculate_section_score({"contact": "present", "summary": "weak"}) == pytest.approx(1.5 / 7)


def test_calculate_overall_score_uses_documented_weights() -> None:
    assert calculate_overall_score(
        semantic_similarity=0.82,
        keyword_match_ratio=0.70,
        section_score=0.75,
    ) == 77


def test_calculate_overall_score_clamps_inputs_and_output() -> None:
    assert calculate_overall_score(2.0, 2.0, 2.0) == 100
    assert calculate_overall_score(-1.0, -1.0, -1.0) == 0

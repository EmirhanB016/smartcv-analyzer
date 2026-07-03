from app.services.feedback import (
    generate_keyword_suggestion,
    generate_score_summary,
    generate_section_suggestions,
    generate_suggestions,
    get_score_category,
)


def test_get_score_category_boundaries() -> None:
    assert get_score_category(0) == "low"
    assert get_score_category(39) == "low"
    assert get_score_category(40) == "moderate"
    assert get_score_category(64) == "moderate"
    assert get_score_category(65) == "good"
    assert get_score_category(84) == "good"
    assert get_score_category(85) == "strong"
    assert get_score_category(100) == "strong"


def test_generate_score_summary_for_each_category() -> None:
    assert "düşük" in generate_score_summary(20)
    assert "kısmi" in generate_score_summary(50)
    assert "genel olarak uyumlu" in generate_score_summary(75)
    assert "güçlü" in generate_score_summary(92)


def test_generate_keyword_suggestion_mentions_missing_keywords_safely() -> None:
    suggestion = generate_keyword_suggestion(
        ["Python", "FastAPI", "Docker", "SQL", "React", "Kubernetes"]
    )

    assert suggestion is not None
    assert "Eğer bu alanlarda deneyiminiz varsa" in suggestion
    assert "Python, FastAPI, Docker, SQL ve React" in suggestion
    assert "Kubernetes" not in suggestion
    assert "ekleyin" not in suggestion


def test_generate_keyword_suggestion_when_no_missing_keywords() -> None:
    suggestion = generate_keyword_suggestion([])

    assert suggestion == "İş ilanındaki ana anahtar kelimeler CV'nizde büyük ölçüde karşılanıyor."


def test_generate_section_suggestions_prioritizes_important_gaps() -> None:
    section_analysis = {
        "contact": {"status": "missing"},
        "summary": {"status": "weak"},
        "skills": {"status": "missing"},
        "experience": {"status": "weak"},
        "projects": {"status": "missing"},
    }

    suggestions = generate_section_suggestions(section_analysis)

    assert suggestions[0].startswith("Yetenekler bölümü")
    assert suggestions[1].startswith("Deneyim bölümünüz")
    assert suggestions[2].startswith("Projeler bölümü")


def test_generate_section_suggestions_accepts_api_style_section_items() -> None:
    section_analysis = [
        {"section": "Contact information", "status": "missing"},
        {"section": "Technical Skills", "status": "weak"},
        {"section": "Work Experience", "status": "present"},
    ]

    suggestions = generate_section_suggestions(section_analysis)

    assert suggestions[0].startswith("Yetenekler bölümü")
    assert suggestions[1].startswith("İletişim bilgileri")


def test_generate_suggestions_limits_count_and_includes_core_feedback() -> None:
    section_analysis = {
        "skills": {"status": "missing"},
        "experience": {"status": "weak"},
        "projects": {"status": "missing"},
        "summary": {"status": "weak"},
        "education": {"status": "missing"},
        "certifications": {"status": "missing"},
        "contact": {"status": "missing"},
    }

    suggestions = generate_suggestions(
        overall_score=32,
        matched_keywords=["Python"],
        missing_keywords=["FastAPI", "Docker", "SQL"],
        section_analysis=section_analysis,
        semantic_similarity=0.35,
    )

    assert 3 <= len(suggestions) <= 7
    assert "düşük düzeyde uyum" in suggestions[0]
    assert any("FastAPI, Docker ve SQL" in suggestion for suggestion in suggestions)
    assert any("Yetenekler bölümü" in suggestion for suggestion in suggestions)


def test_generate_suggestions_when_cv_is_strong_and_keywords_are_covered() -> None:
    section_analysis = {
        "skills": {"status": "present"},
        "experience": {"status": "present"},
        "projects": {"status": "present"},
    }

    suggestions = generate_suggestions(
        overall_score=91,
        matched_keywords=["Python", "FastAPI"],
        missing_keywords=[],
        section_analysis=section_analysis,
        semantic_similarity=0.90,
    )

    assert 3 <= len(suggestions) <= 7
    assert "güçlü düzeyde uyum" in suggestions[0]
    assert any("Python ve FastAPI" in suggestion for suggestion in suggestions)
    assert any("büyük ölçüde karşılanıyor" in suggestion for suggestion in suggestions)
    assert any("güçlü biçimde örtüşüyor" in suggestion for suggestion in suggestions)

from app.services.keywords import extract_keywords, match_keywords


def test_extract_keywords_prioritizes_common_software_terms() -> None:
    job_description = """
    We are looking for a Python developer with Fast API, Docker, SQL,
    REST API, machine learning, React.js, JS, and cloud deployment experience.
    """

    keywords = extract_keywords(job_description)

    assert "Python" in keywords
    assert "FastAPI" in keywords
    assert "Docker" in keywords
    assert "SQL" in keywords
    assert "REST API" in keywords
    assert "machine learning" in keywords
    assert "React" in keywords
    assert "JavaScript" in keywords
    assert "cloud deployment" in keywords
    assert len(keywords) <= 30


def test_extract_keywords_deduplicates_case_insensitively_and_by_synonym() -> None:
    keywords = extract_keywords("JavaScript javascript JS js React.js react")

    assert keywords.count("JavaScript") == 1
    assert keywords.count("React") == 1


def test_extract_keywords_handles_turkish_and_mixed_descriptions() -> None:
    keywords = extract_keywords(
        "Python, Docker ve SQL bilen; veri analizi ve API geliştirme deneyimi olan aday."
    )

    assert "Python" in keywords
    assert "Docker" in keywords
    assert "SQL" in keywords
    assert any(keyword.lower() in {"api", "api geliştirme"} for keyword in keywords)


def test_extract_keywords_avoids_noisy_phrases_around_technical_terms() -> None:
    job_description = """
    Bu rolde alacaks\u0131n\u0131z. Sorumluluklar Python ve FastAPI kullanarak
    REST API geli\u015ftirmek, Docker, SQL, PostgreSQL, GitHub, JavaScript ve
    CI/CD s\u00fcre\u00e7lerinde \u00e7al\u0131\u015fmay\u0131 kapsar.
    """

    keywords = extract_keywords(job_description)

    assert "Python" in keywords
    assert "FastAPI" in keywords
    assert "REST API" in keywords
    assert "Docker" in keywords
    assert "SQL" in keywords
    assert "PostgreSQL" in keywords
    assert "GitHub" in keywords
    assert "JavaScript" in keywords
    assert "CI/CD" in keywords
    assert all("alacaks" not in keyword.casefold() for keyword in keywords)
    assert all("sorumluluk" not in keyword.casefold() for keyword in keywords)
    assert all("kullanarak" not in keyword.casefold() for keyword in keywords)
    assert all(len(keyword.split()) <= 2 for keyword in keywords)


def test_match_keywords_supports_phrases_and_synonyms() -> None:
    cv_text = """
    Built RESTful APIs with Fast API and used JS on frontend projects.
    Worked with ML pipelines and Postgres databases.
    """
    keywords = ["REST API", "FastAPI", "JavaScript", "machine learning", "PostgreSQL", "Docker"]

    result = match_keywords(cv_text, keywords)

    assert result["matched_keywords"] == [
        "REST API",
        "FastAPI",
        "JavaScript",
        "machine learning",
        "PostgreSQL",
    ]
    assert result["missing_keywords"] == ["Docker"]

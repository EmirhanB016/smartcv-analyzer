from app.services.section_detection import (
    detect_contact_info,
    detect_sections,
    extract_section_blocks,
)


def test_detect_sections_with_english_headings() -> None:
    cv_text = """
    Contact
    john@example.com

    Professional Summary
    Backend developer with 5 years of experience building REST APIs and scalable web applications.

    Technical Skills
    Python, FastAPI, Docker, SQL, React, Git

    Work Experience
    Senior Developer at Acme 2020-2024
    - Built REST APIs with FastAPI, Docker, and PostgreSQL.

    Education
    BS Computer Engineering, Example University, 2018

    Projects
    SmartCV Analyzer - FastAPI application with PDF parsing and keyword matching.

    Certifications
    AWS Cloud Practitioner, 2023
    """

    result = detect_sections(cv_text)

    assert result["contact"]["status"] == "present"
    assert result["summary"]["status"] == "present"
    assert result["skills"]["status"] == "present"
    assert result["experience"]["status"] == "present"
    assert result["education"]["status"] == "present"
    assert result["projects"]["status"] == "present"
    assert result["certifications"]["status"] == "present"


def test_detect_sections_with_turkish_headings() -> None:
    cv_text = """
    İletişim
    ayse@example.com

    Özet
    Python ve FastAPI ile backend servisleri geliştiren, Docker ve SQL kullanan yazılım geliştirici.

    Yetenekler
    Python, FastAPI, Docker, PostgreSQL, Git

    İş Deneyimi
    Yazılım Geliştirici - 2021-2024
    - REST API servisleri geliştirdim ve Docker ile dağıtım süreçlerine destek oldum.

    Eğitim
    Bilgisayar Mühendisliği Lisans, 2020

    Projeler
    CV analiz uygulaması - FastAPI, PDF metin çıkarma ve anahtar kelime eşleştirme.

    Sertifikalar
    Python Programlama Sertifikası, 2022
    """

    result = detect_sections(cv_text)

    assert result["summary"]["status"] == "present"
    assert result["skills"]["status"] == "present"
    assert result["experience"]["status"] == "present"
    assert result["education"]["status"] == "present"
    assert result["projects"]["status"] == "present"
    assert result["certifications"]["status"] == "present"


def test_missing_sections_are_reported_as_missing() -> None:
    result = detect_sections("John Doe\njohn@example.com\nPython developer")

    assert result["contact"]["status"] == "present"
    assert result["summary"]["status"] == "missing"
    assert result["skills"]["status"] == "missing"
    assert result["experience"]["status"] == "missing"
    assert result["education"]["status"] == "missing"
    assert result["projects"]["status"] == "missing"
    assert result["certifications"]["status"] == "missing"


def test_weak_sections_are_detected() -> None:
    cv_text = """
    Summary
    Hardworking team player.

    Skills
    Python

    Projects
    Portfolio
    """

    result = detect_sections(cv_text)

    assert result["summary"]["status"] == "weak"
    assert result["skills"]["status"] == "weak"
    assert result["projects"]["status"] == "weak"


def test_contact_detection_uses_email_phone_github_and_linkedin() -> None:
    cv_text = """
    Jane Doe
    +90 555 123 45 67
    https://github.com/janedoe
    https://linkedin.com/in/janedoe
    """

    assert detect_contact_info(cv_text)["status"] == "present"
    assert detect_sections(cv_text)["contact"]["status"] == "present"


def test_extract_section_blocks_supports_inline_heading_content() -> None:
    blocks = extract_section_blocks(
        "Skills: Python, Docker, SQL\nExperience - Built FastAPI services in 2023"
    )

    assert blocks["skills"] == "Python, Docker, SQL"
    assert blocks["experience"] == "Built FastAPI services in 2023"

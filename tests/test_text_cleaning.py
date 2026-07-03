from app.utils.text_cleaning import clean_text, normalize_for_matching


def test_clean_text_normalizes_whitespace_and_blank_lines() -> None:
    text = "  Python\t\tdeveloper  \n\n\n  FastAPI   Docker  "

    assert clean_text(text) == "Python developer\n\nFastAPI Docker"


def test_clean_text_preserves_turkish_display_characters() -> None:
    text = "  İş deneyimi: Çalışkan, ölçülebilir başarılar.  "

    assert clean_text(text) == "İş deneyimi: Çalışkan, ölçülebilir başarılar."


def test_normalize_for_matching_creates_lowercase_matching_copy() -> None:
    text = "İş Deneyimi: Python, FastAPI ve REST API"

    assert normalize_for_matching(text) == "is deneyimi python fastapi ve rest api"

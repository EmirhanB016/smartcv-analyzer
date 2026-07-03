"""Text cleaning and normalization helpers."""

import re
import unicodedata

_INTERNAL_WHITESPACE_RE = re.compile(r"[ \t\f\v]+")
_MULTIPLE_SPACES_RE = re.compile(r"\s+")
_NON_MATCHING_CHAR_RE = re.compile(r"[^a-z0-9+#]+")

_TURKISH_TRANSLATION = str.maketrans(
    {
        "ç": "c",
        "ğ": "g",
        "ı": "i",
        "ö": "o",
        "ş": "s",
        "ü": "u",
    }
)


def clean_text(text: str) -> str:
    """Normalize spacing while preserving display characters."""
    if not text:
        return ""

    normalized_text = (
        text.replace("\r\n", "\n")
        .replace("\r", "\n")
        .replace("\u00a0", " ")
    )

    lines: list[str] = []
    previous_line_was_blank = False

    for raw_line in normalized_text.split("\n"):
        line = _INTERNAL_WHITESPACE_RE.sub(" ", raw_line).strip()
        if not line:
            if lines and not previous_line_was_blank:
                lines.append("")
            previous_line_was_blank = True
            continue

        lines.append(line)
        previous_line_was_blank = False

    return "\n".join(lines).strip()


def normalize_for_matching(text: str) -> str:
    """Create a lowercase ASCII-ish copy for deterministic matching."""
    cleaned_text = clean_text(text).casefold()
    cleaned_text = unicodedata.normalize("NFKD", cleaned_text)
    cleaned_text = "".join(
        character for character in cleaned_text if not unicodedata.combining(character)
    )
    cleaned_text = cleaned_text.translate(_TURKISH_TRANSLATION)
    cleaned_text = cleaned_text.replace("c++", "cplusplus")
    cleaned_text = cleaned_text.replace("c#", "csharp")
    cleaned_text = _NON_MATCHING_CHAR_RE.sub(" ", cleaned_text)
    cleaned_text = cleaned_text.replace("cplusplus", "c++")
    cleaned_text = cleaned_text.replace("csharp", "c#")
    return _MULTIPLE_SPACES_RE.sub(" ", cleaned_text).strip()

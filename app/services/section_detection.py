"""Rule-based CV section detection."""

from collections.abc import Sequence
import re

from app.utils.text_cleaning import clean_text, normalize_for_matching

SectionStatus = str

SECTION_ORDER = (
    "contact",
    "summary",
    "skills",
    "experience",
    "education",
    "projects",
    "certifications",
)

SECTION_HEADINGS = {
    "contact": (
        "contact",
        "contact information",
        "personal information",
        "iletişim",
        "iletişim bilgileri",
        "kişisel bilgiler",
    ),
    "summary": (
        "summary",
        "profile",
        "professional summary",
        "career objective",
        "about me",
        "özet",
        "profil",
        "hakkımda",
        "kariyer hedefi",
        "profesyonel özet",
    ),
    "skills": (
        "skills",
        "technical skills",
        "technologies",
        "core competencies",
        "yetenekler",
        "teknik beceriler",
        "beceriler",
        "teknolojiler",
        "uzmanlıklar",
    ),
    "experience": (
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "iş deneyimi",
        "deneyim",
        "profesyonel deneyim",
        "çalışma deneyimi",
        "kariyer geçmişi",
    ),
    "education": (
        "education",
        "academic background",
        "eğitim",
        "eğitim bilgileri",
        "akademik geçmiş",
    ),
    "projects": (
        "projects",
        "personal projects",
        "project experience",
        "projeler",
        "kişisel projeler",
        "proje deneyimi",
    ),
    "certifications": (
        "certifications",
        "certificates",
        "courses",
        "training",
        "sertifikalar",
        "belgeler",
        "kurslar",
        "eğitimler",
    ),
}

NORMALIZED_SECTION_HEADINGS = {
    section: {normalize_for_matching(heading) for heading in headings}
    for section, headings in SECTION_HEADINGS.items()
}

SECTION_MIN_MEANINGFUL_TOKENS = {
    "summary": 8,
    "skills": 3,
    "experience": 10,
    "education": 3,
    "projects": 8,
    "certifications": 2,
}

GENERIC_WORDS = {
    "acik",
    "adaptable",
    "basarili",
    "caliskan",
    "communicative",
    "deneyim",
    "deneyimli",
    "detail",
    "dynamic",
    "ekip",
    "excellent",
    "gelisime",
    "good",
    "hardworking",
    "iletisim",
    "iyi",
    "motivated",
    "oyuncusu",
    "proactive",
    "responsible",
    "sonuc",
    "strong",
    "takim",
    "team",
    "uyumlu",
}

DETAIL_TERMS = {
    "api",
    "aws",
    "azure",
    "backend",
    "css",
    "database",
    "django",
    "docker",
    "fastapi",
    "frontend",
    "git",
    "html",
    "java",
    "javascript",
    "kubernetes",
    "linux",
    "mongodb",
    "postgres",
    "python",
    "react",
    "redis",
    "rest",
    "sql",
    "typescript",
}

EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
PHONE_RE = re.compile(r"(?:\+?\d[\d\s().-]{7,}\d)")
LINKEDIN_RE = re.compile(r"(?:https?://)?(?:www\.)?linkedin\.com/\S+", re.IGNORECASE)
GITHUB_RE = re.compile(r"(?:https?://)?(?:www\.)?github\.com/\S+", re.IGNORECASE)


def detect_sections(cv_text: str) -> dict[str, dict[str, str]]:
    """Detect expected CV sections and return deterministic Turkish messages."""
    section_blocks = extract_section_blocks(cv_text)

    results: dict[str, dict[str, str]] = {}
    for section_name in SECTION_ORDER:
        section_text = section_blocks.get(section_name, "")
        status = classify_section_status(section_name, section_text, cv_text)
        results[section_name] = {
            "status": status,
            "message": generate_section_message(section_name, status),
        }

    return results


def detect_contact_info(cv_text: str) -> dict[str, str]:
    """Detect contact signals without requiring an explicit heading."""
    status = "present" if _has_contact_signal(cv_text) else "missing"
    return {
        "status": status,
        "message": generate_section_message("contact", status),
    }


def extract_section_blocks(cv_text: str) -> dict[str, str]:
    """Extract text blocks beneath recognized CV headings."""
    cleaned_text = clean_text(cv_text)
    if not cleaned_text:
        return {}

    lines = cleaned_text.splitlines()
    headings: list[tuple[int, str, str]] = []

    for index, line in enumerate(lines):
        detected_heading = _detect_heading(line)
        if detected_heading is not None:
            section_name, inline_content = detected_heading
            headings.append((index, section_name, inline_content))

    section_blocks: dict[str, list[str]] = {}
    for heading_index, (line_index, section_name, inline_content) in enumerate(headings):
        next_line_index = (
            headings[heading_index + 1][0]
            if heading_index + 1 < len(headings)
            else len(lines)
        )
        block_lines = []
        if inline_content:
            block_lines.append(inline_content)
        block_lines.extend(lines[line_index + 1 : next_line_index])

        block_text = clean_text("\n".join(block_lines))
        if block_text:
            section_blocks.setdefault(section_name, []).append(block_text)

    return {
        section_name: clean_text("\n\n".join(blocks))
        for section_name, blocks in section_blocks.items()
    }


def classify_section_status(section_name: str, section_text: str, cv_text: str = "") -> SectionStatus:
    """Classify a section as present, weak, or missing."""
    if section_name == "contact":
        if _has_contact_signal(cv_text):
            return "present"
        if section_text:
            return "weak"
        return "missing"

    if not section_text:
        return "missing"

    meaningful_tokens = _meaningful_tokens(section_text)
    if len(meaningful_tokens) < SECTION_MIN_MEANINGFUL_TOKENS.get(section_name, 5):
        return "weak"

    if _is_generic(section_text, meaningful_tokens):
        return "weak"

    if section_name in {"skills", "experience", "projects"} and not _has_useful_detail(section_text):
        return "weak"

    return "present"


def generate_section_message(section_name: str, status: SectionStatus) -> str:
    """Return the Turkish message for a section result."""
    return SECTION_MESSAGES[section_name][status]


def _detect_heading(line: str) -> tuple[str, str] | None:
    normalized_line = normalize_for_matching(_strip_heading_prefix(line))
    if not normalized_line:
        return None

    for section_name, headings in NORMALIZED_SECTION_HEADINGS.items():
        for heading in headings:
            if normalized_line == heading:
                return section_name, ""
            if normalized_line.startswith(f"{heading} ") and _has_inline_heading_separator(line):
                return section_name, _inline_heading_content(line)

    return None


def _strip_heading_prefix(line: str) -> str:
    return line.strip().strip("•*-_—–| ")


def _has_inline_heading_separator(line: str) -> bool:
    return any(separator in line for separator in (":", "-", "—", "–", "|"))


def _inline_heading_content(line: str) -> str:
    for separator in (":", "—", "–", "|", "-"):
        if separator in line:
            return line.split(separator, maxsplit=1)[1].strip()
    return ""


def _has_contact_signal(text: str) -> bool:
    return (
        EMAIL_RE.search(text) is not None
        or _has_phone_number(text)
        or LINKEDIN_RE.search(text) is not None
        or GITHUB_RE.search(text) is not None
    )


def _has_phone_number(text: str) -> bool:
    for match in PHONE_RE.finditer(text):
        digits = re.sub(r"\D", "", match.group(0))
        if len(digits) >= 10:
            return True
    return False


def _meaningful_tokens(text: str) -> list[str]:
    normalized_text = normalize_for_matching(text)
    return [
        token
        for token in normalized_text.split()
        if len(token) > 1 and token not in GENERIC_WORDS
    ]


def _is_generic(text: str, meaningful_tokens: Sequence[str]) -> bool:
    normalized_tokens = normalize_for_matching(text).split()
    if not normalized_tokens:
        return True

    generic_count = sum(1 for token in normalized_tokens if token in GENERIC_WORDS)
    return generic_count / len(normalized_tokens) >= 0.5 or not meaningful_tokens


def _has_useful_detail(text: str) -> bool:
    normalized_text = normalize_for_matching(text)
    tokens = set(normalized_text.split())
    has_technical_term = bool(tokens & DETAIL_TERMS)
    has_number_or_metric = bool(re.search(r"\d", text))
    has_structured_detail = any(marker in text for marker in ("-", "•", ":", ","))
    return has_technical_term or has_number_or_metric or has_structured_detail


SECTION_MESSAGES = {
    "contact": {
        "present": "İletişim bilgileri CV içerisinde tespit edildi.",
        "weak": "İletişim bölümü mevcut ancak e-posta, telefon veya LinkedIn/GitHub bilgileri daha net yazılabilir.",
        "missing": "İletişim bilgileri tespit edilemedi. E-posta, telefon ve profesyonel bağlantılarınızı eklemeniz önerilir.",
    },
    "summary": {
        "present": "Özet/profil bölümü CV içerisinde yeterli görünüyor.",
        "weak": "Özet/profil bölümü mevcut ancak daha güçlü ve işe özel hale getirilebilir.",
        "missing": "Özet/profil bölümü tespit edilemedi. Kısa bir profesyonel özet eklemeniz önerilir.",
    },
    "skills": {
        "present": "Yetenekler bölümü CV içerisinde tespit edildi.",
        "weak": "Yetenekler bölümü mevcut ancak teknik beceriler daha net ve detaylı listelenebilir.",
        "missing": "Yetenekler bölümü tespit edilemedi. Teknik becerilerinizi ayrı bir bölümde listelemeniz önerilir.",
    },
    "experience": {
        "present": "İş deneyimi bölümü CV içerisinde tespit edildi.",
        "weak": "İş deneyimi bölümü mevcut ancak sorumluluklar, teknolojiler veya ölçülebilir etkiler daha net yazılabilir.",
        "missing": "İş deneyimi bölümü tespit edilemedi. Deneyimlerinizi ayrı bir bölümde açıklamanız önerilir.",
    },
    "education": {
        "present": "Eğitim bölümü CV içerisinde tespit edildi.",
        "weak": "Eğitim bölümü mevcut ancak okul, bölüm, derece veya tarih bilgileri daha net yazılabilir.",
        "missing": "Eğitim bölümü tespit edilemedi. Eğitim bilgilerinizi eklemeniz önerilir.",
    },
    "projects": {
        "present": "Projeler bölümü CV içerisinde tespit edildi.",
        "weak": "Projeler bölümü mevcut ancak kullanılan teknolojiler, sorumluluklar ve çıktılar daha net yazılabilir.",
        "missing": "Projeler bölümü tespit edilemedi. İlgili projelerinizi ayrı bir bölümde göstermeniz önerilir.",
    },
    "certifications": {
        "present": "Sertifikalar/kurslar bölümü CV içerisinde tespit edildi.",
        "weak": "Sertifikalar/kurslar bölümü mevcut ancak kurum, konu veya tarih bilgileri daha net yazılabilir.",
        "missing": "Sertifikalar veya kurslar bölümü tespit edilemedi. Varsa ilgili belgelerinizi ekleyebilirsiniz.",
    },
}

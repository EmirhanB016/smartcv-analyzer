"""Deterministic Turkish feedback generation."""

from collections.abc import Mapping, Sequence
from typing import Any

SECTION_PRIORITY = (
    "skills",
    "experience",
    "projects",
    "summary",
    "education",
    "certifications",
    "contact",
)

SECTION_ALIASES = {
    "contact information": "contact",
    "professional summary": "summary",
    "profile": "summary",
    "technical skills": "skills",
    "work experience": "experience",
    "professional experience": "experience",
    "academic background": "education",
    "personal projects": "projects",
    "project experience": "projects",
    "certificates": "certifications",
    "courses": "certifications",
}

MAX_MISSING_KEYWORDS_TO_MENTION = 5
MIN_SUGGESTIONS = 3
MAX_SUGGESTIONS = 7

SCORE_SUMMARIES = {
    "low": "CV'niz iş ilanıyla düşük düzeyde uyum gösteriyor. Özellikle teknik beceriler, deneyim ve role özel detaylar güçlendirilebilir.",
    "moderate": "CV'niz iş ilanıyla kısmi düzeyde uyumlu görünüyor. Bazı ilgili bilgiler mevcut ancak eksik anahtar kelimeler ve zayıf bölümler güçlendirilebilir.",
    "good": "CV'niz iş ilanıyla genel olarak uyumlu görünüyor. İlgili becerilerin görünürlüğünü artırmak ve somut başarıları netleştirmek faydalı olabilir.",
    "strong": "CV'niz iş ilanıyla güçlü düzeyde uyum gösteriyor. Küçük düzenlemeler ve role özel vurgularla daha etkili hale getirilebilir.",
}

SECTION_SUGGESTIONS = {
    "skills": {
        "missing": "Yetenekler bölümü tespit edilemedi. Teknik becerilerinizi ayrı ve okunabilir bir bölümde listelemeniz önerilir.",
        "weak": "Yetenekler bölümü mevcut ancak teknik beceriler, araçlar ve seviyeler daha net gruplandırılabilir.",
    },
    "experience": {
        "missing": "Deneyim bölümü tespit edilemedi. Role uygun iş, staj veya gönüllü deneyimlerinizi ayrı bir bölümde açıklamanız önerilir.",
        "weak": "Deneyim bölümünüz mevcut ancak sorumluluklar, kullanılan teknolojiler ve ölçülebilir başarılarla desteklenebilir.",
    },
    "projects": {
        "missing": "Projeler bölümü mevcut değil. İş ilanıyla ilişkili kişisel, akademik veya açık kaynak projelerinizi eklemek CV'nizi güçlendirebilir.",
        "weak": "Projeler bölümü mevcut ancak kullanılan teknolojiler, amaç, katkınız ve çıktılar daha net yazılabilir.",
    },
    "summary": {
        "missing": "Özet/profil bölümü tespit edilemedi. İlgili uzmanlık alanlarınızı ve hedef rolünüzü anlatan kısa bir özet ekleyebilirsiniz.",
        "weak": "Özet/profil bölümü mevcut ancak hedef role daha özel, net ve güçlü hale getirilebilir.",
    },
    "education": {
        "missing": "Eğitim bölümü tespit edilemedi. Okul, bölüm, derece ve tarih bilgilerinizi eklemeniz önerilir.",
        "weak": "Eğitim bölümü mevcut ancak okul, bölüm, derece veya tarih bilgileri daha net yazılabilir.",
    },
    "certifications": {
        "missing": "Sertifikalar veya kurslar bölümü tespit edilemedi. Varsa işle ilgili belgelerinizi görünür hale getirebilirsiniz.",
        "weak": "Sertifikalar/kurslar bölümü mevcut ancak kurum, konu veya tarih bilgileri daha net belirtilebilir.",
    },
    "contact": {
        "missing": "İletişim bilgileri tespit edilemedi. E-posta, telefon ve LinkedIn/GitHub gibi profesyonel bağlantılarınızı eklemeniz önerilir.",
        "weak": "İletişim bölümü mevcut ancak e-posta, telefon veya profesyonel bağlantılar daha net yazılabilir.",
    },
}

FALLBACK_SUGGESTIONS = {
    "low": "CV'nizde ilanla ilişkili sorumlulukları, teknik araçları ve somut çıktıları daha açık şekilde vurgulamanız önerilir.",
    "moderate": "İlgili deneyimlerinizi ilan diline daha yakın başlıklar ve örneklerle görünür hale getirebilirsiniz.",
    "good": "Güçlü görünen bölümlere ölçülebilir başarılar, proje çıktıları ve kullanılan teknolojiler eklemek etkiyi artırabilir.",
    "strong": "CV'nizi başvurduğunuz role göre küçük ifadelerle özelleştirmeniz son dokunuş için yeterli olabilir.",
}


def get_score_category(overall_score: int) -> str:
    """Return the deterministic score category for an overall score."""
    score = max(0, min(100, int(overall_score)))
    if score <= 39:
        return "low"
    if score <= 64:
        return "moderate"
    if score <= 84:
        return "good"
    return "strong"


def generate_score_summary(overall_score: int) -> str:
    """Generate the score-based Turkish summary sentence."""
    return SCORE_SUMMARIES[get_score_category(overall_score)]


def generate_keyword_suggestion(missing_keywords: list[str]) -> str | None:
    """Generate a safe keyword suggestion without encouraging false claims."""
    if not missing_keywords:
        return "İş ilanındaki ana anahtar kelimeler CV'nizde büyük ölçüde karşılanıyor."

    keyword_text = _format_keyword_list(missing_keywords[:MAX_MISSING_KEYWORDS_TO_MENTION])
    return (
        "Eğer bu alanlarda deneyiminiz varsa, "
        f"{keyword_text} gibi anahtar kelimeleri CV'nizde daha görünür hale getirebilirsiniz."
    )


def generate_section_suggestions(section_analysis: Mapping[str, Any] | Sequence[Any]) -> list[str]:
    """Generate prioritized suggestions for missing or weak CV sections."""
    normalized_sections = _normalize_section_analysis(section_analysis)
    suggestions: list[str] = []

    for section_name in SECTION_PRIORITY:
        status = normalized_sections.get(section_name)
        if status in {"missing", "weak"}:
            suggestions.append(SECTION_SUGGESTIONS[section_name][status])

    return suggestions


def generate_suggestions(
    overall_score: int,
    matched_keywords: list[str],
    missing_keywords: list[str],
    section_analysis: Mapping[str, Any] | Sequence[Any],
    semantic_similarity: float | None = None,
) -> list[str]:
    """Generate a concise deterministic Turkish suggestion list."""
    score_category = get_score_category(overall_score)
    suggestions = [generate_score_summary(overall_score)]

    keyword_suggestion = (
        generate_keyword_suggestion(missing_keywords)
        if missing_keywords
        else _generate_matched_keyword_suggestion(matched_keywords)
    )
    if keyword_suggestion is not None:
        suggestions.append(keyword_suggestion)

    suggestions.extend(generate_section_suggestions(section_analysis))

    semantic_suggestion = _generate_semantic_similarity_suggestion(semantic_similarity)
    if semantic_suggestion:
        suggestions.append(semantic_suggestion)

    if len(suggestions) < MIN_SUGGESTIONS:
        suggestions.append(FALLBACK_SUGGESTIONS[score_category])

    return _deduplicate_preserving_order(suggestions)[:MAX_SUGGESTIONS]


def _generate_semantic_similarity_suggestion(semantic_similarity: float | None) -> str | None:
    if semantic_similarity is None:
        return None

    if semantic_similarity < 0.45:
        return "CV'nizin genel anlatımı iş ilanıyla zayıf benzerlik gösteriyor. Deneyimlerinizi hedef rolün diliyle daha açık ilişkilendirebilirsiniz."

    if semantic_similarity >= 0.85:
        return "CV'nizin genel anlatımı iş ilanıyla güçlü biçimde örtüşüyor. Son düzenlemede gereksiz tekrarları azaltmanız yeterli olabilir."

    return None


def _generate_matched_keyword_suggestion(matched_keywords: Sequence[str]) -> str:
    if not matched_keywords:
        return generate_keyword_suggestion([]) or ""

    keyword_text = _format_keyword_list(matched_keywords[:MAX_MISSING_KEYWORDS_TO_MENTION])
    return (
        f"{keyword_text} gibi ana anahtar kelimeler CV'nizde büyük ölçüde karşılanıyor ve görünür durumda."
    )


def _normalize_section_analysis(
    section_analysis: Mapping[str, Any] | Sequence[Any],
) -> dict[str, str]:
    if isinstance(section_analysis, Mapping):
        return {
            _canonical_section_name(section): _extract_status(value)
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
            normalized_sections[_canonical_section_name(section)] = _normalize_status(status)

    return normalized_sections


def _canonical_section_name(section: Any) -> str:
    normalized_section = str(section).casefold()
    return SECTION_ALIASES.get(normalized_section, normalized_section)


def _extract_status(value: Any) -> str:
    if isinstance(value, Mapping):
        return _normalize_status(value.get("status"))
    return _normalize_status(value)


def _normalize_status(status: Any) -> str:
    normalized_status = str(status or "").casefold()
    if normalized_status in {"present", "weak", "missing"}:
        return normalized_status
    return "missing"


def _format_keyword_list(keywords: Sequence[str]) -> str:
    if len(keywords) == 1:
        return keywords[0]
    if len(keywords) == 2:
        return f"{keywords[0]} ve {keywords[1]}"
    return f"{', '.join(keywords[:-1])} ve {keywords[-1]}"


def _deduplicate_preserving_order(suggestions: Sequence[str]) -> list[str]:
    seen: set[str] = set()
    unique_suggestions: list[str] = []

    for suggestion in suggestions:
        if suggestion not in seen:
            seen.add(suggestion)
            unique_suggestions.append(suggestion)

    return unique_suggestions

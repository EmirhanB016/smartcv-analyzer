"""Rule-based keyword extraction and matching."""

from dataclasses import dataclass
import re

from app.utils.text_cleaning import clean_text, normalize_for_matching

DEFAULT_MAX_KEYWORDS = 30

TOKEN_RE = re.compile(r"[A-Za-zÇĞİÖŞÜçğıöşü0-9+#./-]+")

ENGLISH_STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "can",
    "for",
    "from",
    "have",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "our",
    "that",
    "the",
    "this",
    "to",
    "we",
    "with",
    "you",
    "your",
}

TURKISH_STOP_WORDS = {
    "ama",
    "ancak",
    "bir",
    "bu",
    "cok",
    "da",
    "daha",
    "de",
    "en",
    "gibi",
    "icin",
    "ile",
    "ise",
    "mi",
    "olan",
    "olarak",
    "ve",
    "veya",
    "ya",
}

GENERIC_TERMS = {
    "ability",
    "aranan",
    "candidate",
    "candidates",
    "developer",
    "development",
    "deneyim",
    "deneyimi",
    "ekip",
    "excellent",
    "experience",
    "experienced",
    "good",
    "gorev",
    "gorevler",
    "guc",
    "guzel",
    "high",
    "iyi",
    "job",
    "knowledge",
    "looking",
    "pozisyon",
    "required",
    "requirements",
    "responsibilities",
    "role",
    "skills",
    "strong",
    "team",
    "work",
}

STOP_WORDS = ENGLISH_STOP_WORDS | TURKISH_STOP_WORDS | GENERIC_TERMS

CANONICAL_DISPLAY = {
    "agile": "Agile",
    "api": "API",
    "artificial intelligence": "artificial intelligence",
    "aws": "AWS",
    "azure": "Azure",
    "backend": "backend",
    "c#": "C#",
    "c++": "C++",
    "ci/cd": "CI/CD",
    "cloud": "cloud",
    "cloud deployment": "cloud deployment",
    "css": "CSS",
    "devops": "DevOps",
    "django": "Django",
    "docker": "Docker",
    "fastapi": "FastAPI",
    "flask": "Flask",
    "frontend": "frontend",
    "git": "Git",
    "github": "GitHub",
    "gitlab": "GitLab",
    "html": "HTML",
    "java": "Java",
    "javascript": "JavaScript",
    "kubernetes": "Kubernetes",
    "machine learning": "machine learning",
    "microservices": "microservices",
    "mongodb": "MongoDB",
    "mysql": "MySQL",
    "nextjs": "Next.js",
    "node": "Node.js",
    "postgres": "PostgreSQL",
    "python": "Python",
    "react": "React",
    "redis": "Redis",
    "rest api": "REST API",
    "sql": "SQL",
    "typescript": "TypeScript",
    "vue": "Vue",
}

SYNONYM_VARIANTS = {
    "ai": "artificial intelligence",
    "artificial intelligence": "artificial intelligence",
    "ci cd": "ci/cd",
    "ci/cd": "ci/cd",
    "continuous integration": "ci/cd",
    "fast api": "fastapi",
    "fastapi": "fastapi",
    "js": "javascript",
    "javascript": "javascript",
    "ml": "machine learning",
    "machine learning": "machine learning",
    "node": "node",
    "node js": "node",
    "node.js": "node",
    "postgres": "postgres",
    "postgresql": "postgres",
    "react": "react",
    "react js": "react",
    "react.js": "react",
    "rest api": "rest api",
    "rest apis": "rest api",
    "restful api": "rest api",
    "restful apis": "rest api",
    "ts": "typescript",
    "typescript": "typescript",
}

TECHNICAL_TERMS = set(CANONICAL_DISPLAY) | {
    "analytics",
    "automation",
    "database",
    "deployment",
    "etl",
    "linux",
    "mobile",
    "nosql",
    "orm",
    "pipeline",
    "testing",
    "ux",
}

IMPORTANT_PHRASES = {
    "api development",
    "backend development",
    "cloud deployment",
    "data analysis",
    "data engineering",
    "database design",
    "frontend development",
    "mobile development",
    "software development",
    "unit testing",
    "web development",
}

METHODOLOGY_TERMS = {
    "agile",
    "ci/cd",
    "devops",
    "scrum",
    "testing",
    "unit testing",
}


@dataclass
class _KeywordCandidate:
    display: str
    score: int
    position: int


def extract_keywords(job_description: str, max_keywords: int = DEFAULT_MAX_KEYWORDS) -> list[str]:
    """Extract readable, deduplicated keywords from a job description."""
    cleaned_text = clean_text(job_description)
    if not cleaned_text:
        return []

    normalized_text = normalize_for_matching(cleaned_text)
    candidates: dict[str, _KeywordCandidate] = {}

    _add_known_term_candidates(candidates, normalized_text)
    _add_ngram_candidates(candidates, cleaned_text)

    ordered_candidates = sorted(
        candidates.values(),
        key=lambda candidate: (-candidate.score, candidate.position, candidate.display.lower()),
    )
    return [candidate.display for candidate in ordered_candidates[:max_keywords]]


def match_keywords(cv_text: str, keywords: list[str]) -> dict[str, list[str]]:
    """Split keywords into matched and missing lists by searching CV text."""
    normalized_cv_text = normalize_for_matching(cv_text)
    matched_keywords: list[str] = []
    missing_keywords: list[str] = []

    for keyword in keywords:
        canonical_keyword = canonicalize_keyword(keyword)
        variants = _variants_for(canonical_keyword)
        if any(_contains_phrase(normalized_cv_text, variant) for variant in variants):
            matched_keywords.append(keyword)
        else:
            missing_keywords.append(keyword)

    return {
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
    }


def canonicalize_keyword(keyword: str) -> str:
    """Normalize a keyword to its canonical matching form."""
    normalized_keyword = normalize_for_matching(keyword)
    return SYNONYM_VARIANTS.get(normalized_keyword, normalized_keyword)


def _add_known_term_candidates(
    candidates: dict[str, _KeywordCandidate],
    normalized_text: str,
) -> None:
    for variant, canonical in sorted(SYNONYM_VARIANTS.items(), key=lambda item: -len(item[0])):
        position = _find_phrase_position(normalized_text, variant)
        if position >= 0:
            _add_candidate(
                candidates,
                canonical=canonical,
                display=CANONICAL_DISPLAY.get(canonical, variant),
                score=40 + len(canonical.split()),
                position=position,
            )

    for canonical, display in CANONICAL_DISPLAY.items():
        position = _find_phrase_position(normalized_text, canonical)
        if position >= 0:
            _add_candidate(
                candidates,
                canonical=canonical,
                display=display,
                score=35 + len(canonical.split()),
                position=position,
            )


def _add_ngram_candidates(
    candidates: dict[str, _KeywordCandidate],
    cleaned_text: str,
) -> None:
    token_pairs = _token_pairs(cleaned_text)

    for size in (1, 2, 3):
        for index in range(0, len(token_pairs) - size + 1):
            display_tokens = [pair[0] for pair in token_pairs[index : index + size]]
            normalized_tokens = [pair[1] for pair in token_pairs[index : index + size]]
            canonical = " ".join(normalized_tokens)

            if not _is_useful_ngram(normalized_tokens, canonical):
                continue

            canonical = canonicalize_keyword(canonical)
            display = CANONICAL_DISPLAY.get(canonical, " ".join(display_tokens))
            _add_candidate(
                candidates,
                canonical=canonical,
                display=display,
                score=_score_ngram(normalized_tokens, canonical),
                position=index,
            )


def _token_pairs(text: str) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for token in TOKEN_RE.findall(text):
        normalized_parts = normalize_for_matching(token).split()
        if len(normalized_parts) == 1:
            pairs.append((token, normalized_parts[0]))

    return pairs


def _is_useful_ngram(tokens: list[str], canonical: str) -> bool:
    if any(token in STOP_WORDS for token in tokens):
        return False

    if canonical in SYNONYM_VARIANTS or canonical in IMPORTANT_PHRASES:
        return True

    if len(tokens) == 1:
        token = tokens[0]
        return token in TECHNICAL_TERMS or token in METHODOLOGY_TERMS

    return (
        any(token in TECHNICAL_TERMS for token in tokens)
        or canonical in METHODOLOGY_TERMS
    )


def _score_ngram(tokens: list[str], canonical: str) -> int:
    score = 10 + len(tokens) * 3
    if canonical in IMPORTANT_PHRASES:
        score += 12
    if canonical in METHODOLOGY_TERMS:
        score += 10
    if canonical in CANONICAL_DISPLAY:
        score += 8
    if any(token in TECHNICAL_TERMS for token in tokens):
        score += 6
    return score


def _add_candidate(
    candidates: dict[str, _KeywordCandidate],
    canonical: str,
    display: str,
    score: int,
    position: int,
) -> None:
    existing_candidate = candidates.get(canonical)
    if existing_candidate is None or score > existing_candidate.score:
        candidates[canonical] = _KeywordCandidate(
            display=display,
            score=score,
            position=position,
        )


def _contains_phrase(normalized_text: str, normalized_phrase: str) -> bool:
    return _find_phrase_position(normalized_text, normalized_phrase) >= 0


def _find_phrase_position(normalized_text: str, normalized_phrase: str) -> int:
    if not normalized_phrase:
        return -1

    pattern = re.compile(
        rf"(?<![a-z0-9+#]){re.escape(normalized_phrase)}(?![a-z0-9+#])"
    )
    match = pattern.search(normalized_text)
    if match is None:
        return -1
    return match.start()


def _variants_for(canonical_keyword: str) -> set[str]:
    variants = {canonical_keyword}
    variants.update(
        variant
        for variant, canonical in SYNONYM_VARIANTS.items()
        if canonical == canonical_keyword
    )
    return variants

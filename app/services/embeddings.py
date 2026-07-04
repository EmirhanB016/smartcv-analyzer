"""Embedding generation and semantic similarity helpers."""

from collections.abc import Sequence
import logging
import math
import re
from typing import Any

from app.core.config import embeddings_enabled
from app.utils.text_cleaning import clean_text
from app.utils.text_cleaning import normalize_for_matching

EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
FALLBACK_SEMANTIC_SIMILARITY_NAME = "token-overlap"

_embedding_model: Any | None = None
_embedding_model_load_failed = False

logger = logging.getLogger(__name__)

_FALLBACK_TOKEN_RE = re.compile(r"[a-z0-9+#]+")
_FALLBACK_STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "is",
    "of",
    "on",
    "or",
    "our",
    "the",
    "to",
    "we",
    "with",
    "you",
    "ve",
    "veya",
    "ile",
    "icin",
    "bir",
    "bu",
    "da",
    "de",
    "olan",
    "olarak",
}


def get_embedding_model() -> Any:
    """Load and cache the sentence-transformers model lazily."""
    global _embedding_model, _embedding_model_load_failed

    if _embedding_model is None:
        if _embedding_model_load_failed:
            raise RuntimeError("Embedding model is unavailable.")

        try:
            from sentence_transformers import SentenceTransformer

            _embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        except Exception:
            _embedding_model_load_failed = True
            logger.warning(
                "Sentence-transformers model could not be loaded; using lightweight semantic similarity fallback.",
                exc_info=True,
            )
            raise
    return _embedding_model


def generate_embedding(text: str, model: Any | None = None) -> list[float]:
    """Generate an embedding for cleaned text.

    Empty text returns an empty vector so callers can handle invalid input without
    forcing model loading.
    """
    cleaned_text = clean_text(text)
    if not cleaned_text:
        return []

    if model is None and not embeddings_enabled():
        return []

    embedding_model = model if model is not None else get_embedding_model()
    embedding = embedding_model.encode(cleaned_text, convert_to_numpy=False)
    return _as_float_list(embedding)


def calculate_cosine_similarity(
    vector_a: Sequence[float],
    vector_b: Sequence[float],
) -> float:
    """Calculate cosine similarity safely for two equal-length vectors."""
    if not vector_a or not vector_b or len(vector_a) != len(vector_b):
        return 0.0

    dot_product = sum(float(a) * float(b) for a, b in zip(vector_a, vector_b))
    norm_a = math.sqrt(sum(float(value) ** 2 for value in vector_a))
    norm_b = math.sqrt(sum(float(value) ** 2 for value in vector_b))

    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0

    return dot_product / (norm_a * norm_b)


def calculate_semantic_similarity(
    cv_text: str,
    job_description: str,
    model: Any | None = None,
) -> float:
    """Calculate clamped semantic similarity between CV and job description."""
    if not clean_text(cv_text) or not clean_text(job_description):
        return 0.0

    if model is None and not embeddings_enabled():
        return calculate_fallback_semantic_similarity(cv_text, job_description)

    try:
        cv_embedding = generate_embedding(cv_text, model=model)
        job_embedding = generate_embedding(job_description, model=model)
        similarity = calculate_cosine_similarity(cv_embedding, job_embedding)
    except Exception:
        logger.warning(
            "Embedding semantic similarity failed; using lightweight fallback.",
            exc_info=True,
        )
        return calculate_fallback_semantic_similarity(cv_text, job_description)

    return _clamp_float(similarity, 0.0, 1.0)


def calculate_fallback_semantic_similarity(cv_text: str, job_description: str) -> float:
    """Calculate lightweight semantic similarity without importing ML libraries."""
    cv_tokens = _extract_fallback_tokens(cv_text)
    job_tokens = _extract_fallback_tokens(job_description)
    if not cv_tokens or not job_tokens:
        return 0.0

    shared_tokens = cv_tokens & job_tokens
    if not shared_tokens:
        return 0.0

    jaccard_similarity = len(shared_tokens) / len(cv_tokens | job_tokens)
    job_coverage = len(shared_tokens) / len(job_tokens)
    cv_coverage = len(shared_tokens) / len(cv_tokens)
    similarity = (job_coverage * 0.65) + (jaccard_similarity * 0.25) + (cv_coverage * 0.10)
    return _clamp_float(similarity, 0.0, 1.0)


def _as_float_list(embedding: Any) -> list[float]:
    if hasattr(embedding, "tolist"):
        embedding = embedding.tolist()

    if (
        isinstance(embedding, Sequence)
        and embedding
        and isinstance(embedding[0], Sequence)
        and not isinstance(embedding[0], (str, bytes))
    ):
        embedding = embedding[0]

    return [float(value) for value in embedding]


def _clamp_float(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, float(value)))


def _extract_fallback_tokens(text: str) -> set[str]:
    normalized_text = normalize_for_matching(text)
    return {
        token
        for token in _FALLBACK_TOKEN_RE.findall(normalized_text)
        if len(token) >= 2 and token not in _FALLBACK_STOP_WORDS
    }

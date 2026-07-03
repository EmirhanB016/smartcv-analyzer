"""Embedding generation and semantic similarity helpers."""

from collections.abc import Sequence
import math
from typing import Any

from app.utils.text_cleaning import clean_text

EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

_embedding_model: Any | None = None


def get_embedding_model() -> Any:
    """Load and cache the sentence-transformers model lazily."""
    global _embedding_model

    if _embedding_model is None:
        from sentence_transformers import SentenceTransformer

        _embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    return _embedding_model


def generate_embedding(text: str, model: Any | None = None) -> list[float]:
    """Generate an embedding for cleaned text.

    Empty text returns an empty vector so callers can handle invalid input without
    forcing model loading.
    """
    cleaned_text = clean_text(text)
    if not cleaned_text:
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

    cv_embedding = generate_embedding(cv_text, model=model)
    job_embedding = generate_embedding(job_description, model=model)
    similarity = calculate_cosine_similarity(cv_embedding, job_embedding)
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

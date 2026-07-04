"""Compatibility wrapper for embedding service functions."""

from app.services.embeddings import (
    EMBEDDING_MODEL_NAME,
    FALLBACK_SEMANTIC_SIMILARITY_NAME,
    calculate_fallback_semantic_similarity,
    calculate_cosine_similarity,
    calculate_semantic_similarity,
    generate_embedding,
    get_embedding_model,
)

__all__ = [
    "EMBEDDING_MODEL_NAME",
    "FALLBACK_SEMANTIC_SIMILARITY_NAME",
    "calculate_fallback_semantic_similarity",
    "calculate_cosine_similarity",
    "calculate_semantic_similarity",
    "generate_embedding",
    "get_embedding_model",
]

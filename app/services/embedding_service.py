"""Compatibility wrapper for embedding service functions."""

from app.services.embeddings import (
    EMBEDDING_MODEL_NAME,
    calculate_cosine_similarity,
    calculate_semantic_similarity,
    generate_embedding,
    get_embedding_model,
)

__all__ = [
    "EMBEDDING_MODEL_NAME",
    "calculate_cosine_similarity",
    "calculate_semantic_similarity",
    "generate_embedding",
    "get_embedding_model",
]

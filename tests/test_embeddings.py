import pytest

from app.services.embeddings import (
    calculate_cosine_similarity,
    calculate_semantic_similarity,
    generate_embedding,
)


class FakeEmbeddingModel:
    def encode(self, text: str, convert_to_numpy: bool = False) -> list[float]:
        if "opposite" in text:
            return [-1.0, 0.0, 0.0]
        if "python" in text.casefold():
            return [1.0, 1.0, 0.0]
        return [1.0, 0.0, 0.0]


def test_generate_embedding_uses_injected_model_without_loading_real_model() -> None:
    embedding = generate_embedding("Python developer", model=FakeEmbeddingModel())

    assert embedding == [1.0, 1.0, 0.0]


def test_generate_embedding_returns_empty_vector_for_empty_text() -> None:
    assert generate_embedding("   ") == []


def test_calculate_cosine_similarity_for_identical_and_orthogonal_vectors() -> None:
    assert calculate_cosine_similarity([1, 2, 3], [1, 2, 3]) == pytest.approx(1.0)
    assert calculate_cosine_similarity([1, 0], [0, 1]) == pytest.approx(0.0)


def test_calculate_cosine_similarity_handles_invalid_vectors_safely() -> None:
    assert calculate_cosine_similarity([], [1, 2]) == 0.0
    assert calculate_cosine_similarity([1, 2], [1]) == 0.0
    assert calculate_cosine_similarity([0, 0], [1, 2]) == 0.0


def test_calculate_semantic_similarity_clamps_negative_similarity() -> None:
    similarity = calculate_semantic_similarity(
        "Python developer",
        "opposite direction",
        model=FakeEmbeddingModel(),
    )

    assert similarity == 0.0


def test_calculate_semantic_similarity_returns_zero_for_empty_inputs() -> None:
    assert calculate_semantic_similarity("", "Python developer", model=FakeEmbeddingModel()) == 0.0
    assert calculate_semantic_similarity("Python developer", "", model=FakeEmbeddingModel()) == 0.0

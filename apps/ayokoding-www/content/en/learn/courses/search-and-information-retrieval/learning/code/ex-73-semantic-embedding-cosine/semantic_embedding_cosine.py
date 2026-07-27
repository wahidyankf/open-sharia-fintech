# pyright: strict
"""Example 73: Semantic Embedding Cosine (co-35)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import math  # => stdlib math -- log/sqrt for idf, cosine, and skip-pointer spacing


def cosine_similarity(
    a: list[float], b: list[float]
) -> float:  # => the Example 27 formula again: dot(a, b) / (|a| * |b|)
    """The Example 27 formula again: dot(a, b) / (|a| * |b|)."""
    dot: float = sum(x * y for x, y in zip(a, b))  # => co-27: the dot product
    norm_a: float = math.sqrt(
        sum(x * x for x in a)
    )  # => co-27: |a|, the Euclidean length of a
    norm_b: float = math.sqrt(
        sum(y * y for y in b)
    )  # => co-27: |b|, the Euclidean length of b
    if norm_a == 0 or norm_b == 0:  # => true when norm_a == 0 or norm_b == 0
        return 0.0  # => returns 0.0
    return dot / (norm_a * norm_b)  # => returns dot / (norm_a * norm_b)


def main() -> None:  # => defines main
    # TOY 3-dimensional embeddings, hand-picked to encode a "vehicle-ness" concept -- NOT from a real model.
    query_vec: list[float] = [
        0.9,
        0.1,
        0.0,
    ]  # => co-35: a query about "cars," represented as a toy vector
    doc_vectors: dict[int, list[float]] = {  # => doc vectors = {
        0: [
            0.85,
            0.15,
            0.05,
        ],  # => doc 0: "automobile" -- semantically close to the query, despite zero word overlap
        1: [0.05, 0.10, 0.95],  # => doc 1: "recipe" -- semantically distant
    }  # => opens/closes this multi-line literal

    scores: dict[
        int, float
    ] = {  # => co-35: EVERY doc's cosine similarity to the query vector
        doc_id: cosine_similarity(query_vec, vec)
        for doc_id, vec in doc_vectors.items()  # => part of this step's computation, continued from the line above
    }  # => opens/closes this multi-line literal
    ranking: list[int] = sorted(
        scores, key=lambda d: -scores[d]
    )  # => co-20: best (highest) similarity first
    for doc_id in ranking:  # => iterates one item at a time
        print(f"doc {doc_id}: cosine={scores[doc_id]:.4f}")  # => shows doc

    assert ranking[0] == 0, (
        "the semantically NEAR document (doc 0) must rank first, by cosine similarity alone"
    )  # => the semantically NEAR document (doc 0) must rank first, by cosine similarity alone
    assert scores[0] > scores[1], (
        "doc 0's similarity must be strictly higher than doc 1's"
    )  # => doc 0's similarity must be strictly higher than doc 1's
    print(
        f"MATCH: the nearest-meaning document ranks first ({scores[0]:.4f} vs {scores[1]:.4f}) using only vector cosine, no shared words"
    )  # => shows MATCH: the nearest-meaning document ranks first (


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end

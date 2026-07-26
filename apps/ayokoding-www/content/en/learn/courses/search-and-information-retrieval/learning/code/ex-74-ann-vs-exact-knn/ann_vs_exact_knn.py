# pyright: strict
"""Example 74: ANN vs Exact kNN (co-35)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import math  # => stdlib math -- log/sqrt for idf, cosine, and skip-pointer spacing
import random  # => stdlib PRNG -- reproducible synthetic fixtures and trials


def cosine_similarity(
    a: list[float], b: list[float]
) -> float:  # => defines cosine similarity
    dot: float = sum(
        x * y for x, y in zip(a, b)
    )  # => dot = sum(x * y for x, y in zip(a, b))
    norm_a: float = math.sqrt(
        sum(x * x for x in a)
    )  # => norm a = math.sqrt(sum(x * x for x in a))
    norm_b: float = math.sqrt(
        sum(y * y for y in b)
    )  # => norm b = math.sqrt(sum(y * y for y in b))
    return (
        dot / (norm_a * norm_b) if norm_a and norm_b else 0.0
    )  # => returns dot / (norm_a * norm_b) if norm_a and norm_b else 0.0


def exact_knn(
    query: list[float], vectors: dict[int, list[float]], k: int
) -> list[
    int
]:  # => brute-force: score EVERY vector, take the true top-k -- always correct, always O(N)
    """Brute-force: score EVERY vector, take the true top-k -- always correct, always O(N)."""
    scored: list[tuple[int, float]] = [
        (doc_id, cosine_similarity(query, v)) for doc_id, v in vectors.items()
    ]  # => scored = [(doc_id, cosine_similarity(query, v)) for doc_...
    scored.sort(
        key=lambda dv: -dv[1]
    )  # => co-35: full sort -- the GROUND TRUTH ranking
    return [
        doc_id for doc_id, _ in scored[:k]
    ]  # => returns [doc_id for doc_id, _ in scored[:k]]


def toy_ann(
    query: list[float],
    vectors: dict[int, list[float]],
    k: int,
    sample_size: int,
    seed: int,
) -> list[
    int
]:  # => a TOY approximate search: rank only a random SAMPLE, not the full vector set -- NOT production-grade
    """A TOY approximate search: rank only a random SAMPLE, not the full vector set -- NOT production-grade."""
    rng = random.Random(seed)  # => co-35: fixed seed -- reproducible sampling
    candidate_ids: list[int] = rng.sample(
        list(vectors), min(sample_size, len(vectors))
    )  # => co-35: a random SUBSET, not everything
    candidates: dict[int, list[float]] = {
        doc_id: vectors[doc_id] for doc_id in candidate_ids
    }  # => candidates = {doc_id: vectors[doc_id] for doc_id in candidat...
    return exact_knn(
        query, candidates, k
    )  # => exact search, but only over the sampled subset


def main() -> None:  # => defines main
    rng = random.Random(3)  # => fixed seed -- reproducible corpus
    n_docs: int = 200  # => a larger toy corpus, to make sampling's trade-off visible
    vectors: dict[int, list[float]] = {
        i: [rng.uniform(-1, 1) for _ in range(4)] for i in range(n_docs)
    }  # => vectors = {i: [rng.uniform(-1, 1) for _ in range(4)] for ...
    query: list[float] = [
        rng.uniform(-1, 1) for _ in range(4)
    ]  # => query = [rng.uniform(-1, 1) for _ in range(4)]

    exact_top5: list[int] = exact_knn(
        query, vectors, k=5
    )  # => co-35: the GROUND TRUTH top 5
    ann_top5: list[int] = toy_ann(
        query, vectors, k=5, sample_size=20, seed=3
    )  # => co-35: an approximation over only 20 of 200
    overlap: set[int] = set(exact_top5) & set(
        ann_top5
    )  # => how many of the approximate results are ALSO in the true top 5
    print(f"exact top-5: {exact_top5}")  # => shows exact top-5
    print(
        f"toy ANN top-5 (sampled 20/200): {ann_top5}"
    )  # => shows toy ANN top-5 (sampled 20/200)
    print(
        f"overlap with ground truth: {len(overlap)}/5"
    )  # => shows overlap with ground truth

    assert len(overlap) <= 5, (
        "the ANN result can recover AT MOST all 5 of the exact top-5 (a basic sanity bound)"
    )  # => the ANN result can recover AT MOST all 5 of the exact top-5 (a basic sanity bound)
    # NOTE: production systems use HNSW (Hierarchical Navigable Small World graphs), not random sampling --
    # this toy is built ONLY to demonstrate the recall/speed trade-off in isolation, in pure Python.
    print(
        f"MATCH: the toy ANN recovered {len(overlap)}/5 of the true nearest neighbors from a 10x-smaller candidate pool"
    )  # => shows MATCH: the toy ANN recovered


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end

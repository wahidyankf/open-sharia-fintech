# pyright: strict
"""Example 74: ANN vs Exact kNN (co-35)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import math  # => stdlib math -- log/sqrt for idf, cosine, and skip-pointer spacing
import random  # => stdlib PRNG -- reproducible synthetic fixtures and trials
import time  # => stdlib timer -- wall-clock measurement, not a benchmark micro-op
from typing import Callable  # => from typing: Callable


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

    assert 0 < len(overlap) < 5, (
        "at this fixed seed the toy ANN must recover SOME but not ALL of the exact top-5 (a falsifiable recall bound, not a set-cardinality tautology)"
    )  # => co-35: this fails if recall COLLAPSES to 0 or the sample ACCIDENTALLY matches perfectly -- both are real, checkable outcomes

    exact_time: float = min(
        _time_call(lambda: exact_knn(query, vectors, k=5)) for _ in range(3)
    )  # => co-35: best of 3 runs -- exact_knn scores ALL 200 vectors
    ann_time: float = min(
        _time_call(lambda: toy_ann(query, vectors, k=5, sample_size=20, seed=3))
        for _ in range(3)
    )  # => co-35: best of 3 runs -- toy_ann scores only the sampled 20
    print(
        f"speed: exact={exact_time * 1000:.3f}ms  toy_ann={ann_time * 1000:.3f}ms  ratio={exact_time / ann_time:.1f}x"
    )  # => shows the wall-clock trade-off the recall bound above does NOT capture

    assert ann_time < exact_time, (
        "the toy ANN must be FASTER than exact search -- it scores 20 candidates, not 200"
    )  # => the toy ANN must be FASTER than exact search -- it scores 20 candidates, not 200
    # NOTE: production systems use HNSW (Hierarchical Navigable Small World graphs), not random sampling --
    # this toy is built ONLY to demonstrate the recall/speed trade-off in isolation, in pure Python.
    if overlap:  # => gate the MATCH banner on the REAL recall bound above, not an unconditional print
        print(
            f"MATCH: the toy ANN recovered {len(overlap)}/5 of the true nearest neighbors from a 10x-smaller candidate pool, {exact_time / ann_time:.1f}x faster"
        )  # => shows MATCH: the toy ANN recovered
    else:
        print(
            "NO MATCH: the toy ANN recovered 0/5 of the true nearest neighbors -- recall collapsed at this sample size"
        )  # => shows NO MATCH: recall collapsed at this sample size


def _time_call(fn: Callable[[], object]) -> float:  # => defines _time_call
    start: float = time.perf_counter()  # => start = time.perf_counter()
    fn()  # => part of this step's computation, continued from the line above
    return time.perf_counter() - start  # => returns time.perf_counter() - start


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end

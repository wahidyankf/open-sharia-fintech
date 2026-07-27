# pyright: strict
"""Example 27: Cosine Similarity (co-15)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import math  # => stdlib math -- log/sqrt for idf, cosine, and skip-pointer spacing


def dot(
    a: dict[str, float], b: dict[str, float]
) -> float:  # => dot product of two sparse vectors -- only shared keys contribute
    """Dot product of two sparse vectors -- only shared keys contribute."""
    return sum(
        weight * b.get(term, 0.0) for term, weight in a.items()
    )  # => co-15: absent keys contribute 0


def norm(vec: dict[str, float]) -> float:  # => euclidean length of a sparse vector
    """Euclidean length of a sparse vector."""
    return math.sqrt(
        sum(w * w for w in vec.values())
    )  # => returns math.sqrt(sum(w * w for w in vec.values()))


def cosine_similarity(
    a: dict[str, float], b: dict[str, float]
) -> float:  # => cosine of the angle between two vectors: dot product / (|a| * |b|)
    """Cosine of the angle between two vectors: dot product / (|a| * |b|)."""
    denom: float = norm(a) * norm(b)  # => denom = norm(a) * norm(b)
    return (
        dot(a, b) / denom if denom > 0 else 0.0
    )  # => co-15: length-normalized -- document length cancels out


def rank_by_cosine(
    query_vec: dict[str, float], doc_vecs: dict[int, dict[str, float]]
) -> list[tuple[int, float]]:  # => defines rank by cosine
    scores: dict[int, float] = {
        doc_id: cosine_similarity(query_vec, vec) for doc_id, vec in doc_vecs.items()
    }  # => scores = {doc_id: cosine_similarity(query_vec, vec) for ...
    return sorted(
        scores.items(), key=lambda kv: (-kv[1], kv[0])
    )  # => returns sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))


def main() -> None:  # => defines main
    query_vec: dict[str, float] = {
        "search": 1.0,
        "fast": 1.0,
    }  # => a simple, unweighted query vector
    doc_vecs: dict[int, dict[str, float]] = {  # => doc vecs = {
        0: {
            "search": 2.0,
            "fast": 1.0,
            "index": 0.5,
        },  # => strongly matches BOTH query terms
        1: {"search": 1.0, "documents": 3.0},  # => matches only ONE query term, weakly
    }  # => opens/closes this multi-line literal
    ranking: list[tuple[int, float]] = rank_by_cosine(
        query_vec, doc_vecs
    )  # => co-15: cosine-ranked results
    for doc_id, score in ranking:  # => iterates one item at a time
        print(f"doc {doc_id}: cosine={score:.4f}")  # => shows doc

    hand_dot_doc0: float = (
        1.0 * 2.0 + 1.0 * 1.0
    )  # => query.search * doc0.search + query.fast * doc0.fast
    hand_norm_q: float = math.sqrt(
        1.0**2 + 1.0**2
    )  # => hand norm q = math.sqrt(1.0**2 + 1.0**2)
    hand_norm_d0: float = math.sqrt(
        2.0**2 + 1.0**2 + 0.5**2
    )  # => hand norm d0 = math.sqrt(2.0**2 + 1.0**2 + 0.5**2)
    hand_cosine_doc0: float = hand_dot_doc0 / (
        hand_norm_q * hand_norm_d0
    )  # => hand cosine doc0 = hand_dot_doc0 / (hand_norm_q * hand_norm_d0)
    assert math.isclose(ranking[0][1], hand_cosine_doc0, abs_tol=1e-9), (
        "doc 0's cosine must match the hand computation"
    )  # => doc 0's cosine must match the hand computation
    assert ranking[0][0] == 0, (
        "doc 0 must rank first -- it matches both query terms strongly"
    )  # => doc 0 must rank first -- it matches both query terms strongly
    print(
        f"MATCH: doc 0's cosine {ranking[0][1]:.4f} equals the hand-computed value {hand_cosine_doc0:.4f}"
    )  # => shows MATCH: doc 0's cosine


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end

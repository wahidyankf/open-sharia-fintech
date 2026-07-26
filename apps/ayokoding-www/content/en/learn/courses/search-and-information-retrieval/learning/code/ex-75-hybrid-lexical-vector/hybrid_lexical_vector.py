# pyright: strict
"""Example 75: Hybrid Lexical + Vector (co-35)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def normalize(
    scores: dict[int, float],
) -> dict[
    int, float
]:  # => min-max normalize a score dict into [0, 1] so lexical and vector scores are comparable
    """Min-max normalize a score dict into [0, 1] so lexical and vector scores are comparable."""
    if not scores:  # => true when not scores
        return {}  # => returns {}
    lo, hi = (
        min(scores.values()),
        max(scores.values()),
    )  # => co-35: the observed range, this corpus's own
    if hi == lo:  # => true when hi == lo
        return {
            doc_id: 1.0 for doc_id in scores
        }  # => returns {doc_id: 1.0 for doc_id in scores}
    return {
        doc_id: (s - lo) / (hi - lo) for doc_id, s in scores.items()
    }  # => co-35: rescaled into [0, 1]


def hybrid_rank(
    bm25_scores: dict[int, float], vector_scores: dict[int, float], alpha: float = 0.5
) -> list[
    int
]:  # => alpha blends the two normalized signals -- alpha=1 is pure lexical, alpha=0 is pure vector
    """alpha blends the two normalized signals -- alpha=1 is pure lexical, alpha=0 is pure vector."""
    norm_bm25: dict[int, float] = normalize(
        bm25_scores
    )  # => co-35: both signals rescaled to the SAME [0, 1] range
    norm_vector: dict[int, float] = normalize(
        vector_scores
    )  # => norm vector = normalize(vector_scores)
    combined: dict[int, float] = {  # => combined = {
        doc_id: alpha * norm_bm25.get(doc_id, 0.0)
        + (1 - alpha) * norm_vector.get(doc_id, 0.0)  # => co-35: the weighted blend
        for doc_id in set(bm25_scores)
        | set(
            vector_scores
        )  # => part of this step's computation, continued from the line above
    }  # => opens/closes this multi-line literal
    return sorted(
        combined, key=lambda d: -combined[d]
    )  # => returns sorted(combined, key=lambda d: -combined[d])


def main() -> None:  # => defines main
    bm25_scores: dict[int, float] = {
        0: 5.0,
        1: 1.0,
        2: 0.2,
    }  # => pure LEXICAL ranking: 0 > 1 > 2
    vector_scores: dict[int, float] = {
        0: 0.1,
        1: 0.9,
        2: 0.95,
    }  # => pure VECTOR ranking: 2 > 1 > 0 -- DISAGREES with BM25

    pure_bm25_ranking: list[int] = sorted(
        bm25_scores, key=lambda d: -bm25_scores[d]
    )  # => the lexical-only order, for comparison
    hybrid: list[int] = hybrid_rank(
        bm25_scores, vector_scores, alpha=0.5
    )  # => co-35: an EQUAL 50/50 blend
    print(f"pure BM25 ranking: {pure_bm25_ranking}")  # => shows pure BM25 ranking
    print(
        f"hybrid ranking (alpha=0.5): {hybrid}"
    )  # => shows hybrid ranking (alpha=0.5)

    assert pure_bm25_ranking == [0, 1, 2], (
        "pure BM25 must rank doc 0 first, given its own scores"
    )  # => pure BM25 must rank doc 0 first, given its own scores
    assert hybrid != pure_bm25_ranking, (
        "the hybrid ranking must DIFFER from pure BM25 when the two signals disagree"
    )  # => the hybrid ranking must DIFFER from pure BM25 when the two signals disagree
    print(
        f"MATCH: blending in the vector signal changed the ranking from {pure_bm25_ranking} to {hybrid}"
    )  # => shows MATCH: blending in the vector signal changed the ranking from


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end

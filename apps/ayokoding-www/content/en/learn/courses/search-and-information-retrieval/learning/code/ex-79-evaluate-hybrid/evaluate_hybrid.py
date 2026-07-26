# pyright: strict
"""Example 79: Evaluate Hybrid (co-22, co-35)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import math  # => stdlib math -- log/sqrt for idf, cosine, and skip-pointer spacing


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


def normalize(scores: dict[int, float]) -> dict[int, float]:  # => defines normalize
    if not scores:  # => true when not scores
        return {}  # => returns {}
    lo, hi = (
        min(scores.values()),
        max(scores.values()),
    )  # => part of this step's computation, continued from the line above
    if hi == lo:  # => true when hi == lo
        return {
            doc_id: 1.0 for doc_id in scores
        }  # => returns {doc_id: 1.0 for doc_id in scores}
    return {
        doc_id: (s - lo) / (hi - lo) for doc_id, s in scores.items()
    }  # => returns {doc_id: (s - lo) / (hi - lo) for doc_id, s in scores.ite...


def precision_at_k(
    ranked: list[int], relevant: set[int], k: int
) -> float:  # => defines precision at k
    top_k: list[int] = ranked[:k]  # => top k = ranked[:k]
    return (
        sum(1 for d in top_k if d in relevant) / k if k > 0 else 0.0
    )  # => returns sum(1 for d in top_k if d in relevant) / k if k > 0 else 0.0


def main() -> None:  # => defines main
    relevant: set[int] = {
        2
    }  # => co-23: doc 2 (the "automobile" doc) is the ONE truly relevant result for this query

    lexical_scores: dict[int, float] = {
        0: 3.0,
        1: 2.0,
        2: 0.0,
    }  # => co-16: doc 2 scores ZERO -- no literal query-term overlap
    vector_scores: dict[int, float] = {
        0: 0.1,
        1: 0.2,
        2: 0.95,
    }  # => co-35: doc 2's embedding is by far the closest

    lexical_ranking: list[int] = sorted(
        lexical_scores, key=lambda d: -lexical_scores[d]
    )  # => co-22: pure lexical order
    alpha: float = 0.3  # => co-35: 30% lexical, 70% vector -- enough weight to let the semantic signal win here
    combined: dict[int, float] = {  # => combined = {
        doc_id: alpha * normalize(lexical_scores).get(doc_id, 0.0)
        + (1 - alpha)
        * normalize(vector_scores).get(
            doc_id, 0.0
        )  # => part of this step's computation, continued from the line above
        for doc_id in lexical_scores  # => part of this step's computation, continued from the line above
    }  # => opens/closes this multi-line literal
    hybrid_ranking: list[int] = sorted(
        combined, key=lambda d: -combined[d]
    )  # => co-35: the alpha-weighted hybrid blend

    p1_lexical: float = precision_at_k(
        lexical_ranking, relevant, k=1
    )  # => co-22: precision@1, lexical only
    p1_hybrid: float = precision_at_k(
        hybrid_ranking, relevant, k=1
    )  # => co-22: precision@1, hybrid
    print(
        f"lexical ranking: {lexical_ranking}  precision@1={p1_lexical:.4f}"
    )  # => shows lexical ranking
    print(
        f"hybrid ranking:  {hybrid_ranking}  precision@1={p1_hybrid:.4f}"
    )  # => shows hybrid ranking

    assert p1_lexical == 0.0, (
        "lexical-only precision@1 must be 0 -- the relevant doc scored zero lexical relevance"
    )  # => lexical-only precision@1 must be 0 -- the relevant doc scored zero lexical relevance
    assert p1_hybrid == 1.0, (
        "hybrid precision@1 must be 1.0 -- the vector signal surfaces the truly relevant doc"
    )  # => hybrid precision@1 must be 1.0 -- the vector signal surfaces the truly relevant doc
    print(
        f"MATCH: hybrid precision@1 ({p1_hybrid}) beats lexical-only ({p1_lexical}) on this synonym-dependent query"
    )  # => shows MATCH: hybrid precision@1 (


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end

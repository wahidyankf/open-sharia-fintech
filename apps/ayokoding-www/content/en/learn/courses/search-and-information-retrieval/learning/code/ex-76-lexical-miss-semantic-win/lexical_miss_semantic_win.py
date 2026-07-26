# pyright: strict
"""Example 76: Lexical Miss, Semantic Win (co-35)."""

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


def lexical_search(
    index: dict[str, set[int]], query_term: str
) -> set[int]:  # => a plain co-04 boolean lookup -- exact term match only
    """A plain co-04 boolean lookup -- exact term match only."""
    return index.get(
        query_term, set()
    )  # => co-04: no match unless the LITERAL term is present


def main() -> None:  # => defines main
    index: dict[str, set[int]] = {
        "automobile": {0},
        "bicycle": {1},
    }  # => NO document literally contains "car"

    query_term: str = "car"  # => co-35: the user's literal query word
    query_vec: list[float] = [0.9, 0.1]  # => a toy embedding for "car"
    doc_vectors: dict[int, list[float]] = {  # => doc vectors = {
        0: [
            0.88,
            0.12,
        ],  # => doc 0's "automobile" embedding -- semantically CLOSE to "car"
        1: [
            0.05,
            0.98,
        ],  # => doc 1's "bicycle" embedding -- semantically FAR from "car"
    }  # => opens/closes this multi-line literal

    lexical_hits: set[int] = lexical_search(
        index, query_term
    )  # => co-04: BM25/boolean search over the literal term
    vector_scores: dict[int, float] = {
        doc_id: cosine_similarity(query_vec, v) for doc_id, v in doc_vectors.items()
    }  # => vector scores = {doc_id: cosine_similarity(query_vec, v) for do...
    semantic_ranking: list[int] = sorted(
        vector_scores, key=lambda d: -vector_scores[d]
    )  # => co-35: ranked by embedding similarity
    print(
        f"lexical search for 'car': {sorted(lexical_hits)}"
    )  # => shows lexical search for 'car'
    print(
        f"semantic ranking: {semantic_ranking} (scores: {vector_scores})"
    )  # => shows semantic ranking

    assert lexical_hits == set(), (
        "lexical (exact-term) search must find NOTHING -- 'car' appears in no document"
    )  # => lexical (exact-term) search must find NOTHING -- 'car' appears in no document
    assert semantic_ranking[0] == 0, (
        "semantic search must rank doc 0 ('automobile') first, despite zero word overlap"
    )  # => semantic search must rank doc 0 ('automobile') first, despite zero word overlap
    print(
        f"MATCH: lexical search found {len(lexical_hits)} docs; semantic search correctly surfaced doc 0 anyway"
    )  # => shows MATCH: lexical search found


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end

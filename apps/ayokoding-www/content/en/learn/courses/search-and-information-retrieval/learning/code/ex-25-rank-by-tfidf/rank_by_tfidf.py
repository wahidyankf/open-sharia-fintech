# pyright: strict
"""Example 25: Rank by TF-IDF (co-14)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import math  # => stdlib math -- log/sqrt for idf, cosine, and skip-pointer spacing


def term_frequency(tokens: list[str]) -> dict[str, int]:  # => defines term frequency
    tf: dict[str, int] = {}  # => starts empty, populated by the loop below
    for term in tokens:  # => iterates one item at a time
        tf[term] = (
            tf.get(term, 0) + 1
        )  # => counter pattern: 0 on first sight, then increments
    return tf  # => returns tf


def document_frequency(
    docs: dict[int, list[str]],
) -> dict[str, int]:  # => defines document frequency
    df: dict[str, int] = {}  # => starts empty, populated by the loop below
    for tokens in docs.values():  # => iterates one item at a time
        for term in set(tokens):  # => iterates one item at a time
            df[term] = (
                df.get(term, 0) + 1
            )  # => counter pattern: 0 on first sight, then increments
    return df  # => returns df


def rank_by_tfidf(
    docs: dict[int, list[str]], query_terms: list[str]
) -> list[
    tuple[int, float]
]:  # => score every doc as the SUM of tf-idf over the query terms it contains, sorted descending
    """Score every doc as the SUM of tf-idf over the query terms it contains, sorted descending."""
    n_docs: int = len(docs)  # => this fixture's own size
    df: dict[str, int] = document_frequency(
        docs
    )  # => co-13: corpus-wide document frequencies
    scores: dict[int, float] = {}  # => starts empty, populated by the loop below
    for doc_id, tokens in docs.items():  # => iterates one item at a time
        tf: dict[str, int] = term_frequency(tokens)  # => tf = term_frequency(tokens)
        score: float = sum(  # => co-14: sum of tf-idf over the terms this doc actually shares with the query
            tf[term] * math.log(n_docs / df[term])
            for term in query_terms
            if term
            in tf  # => part of this step's computation, continued from the line above
        )  # => opens/closes this multi-line literal
        scores[doc_id] = score  # => stores this computed value under its key
    return sorted(
        scores.items(), key=lambda kv: (-kv[1], kv[0])
    )  # => descending score, doc_id as tiebreak


def main() -> None:  # => defines main
    docs: dict[int, list[str]] = {  # => docs = {
        0: [
            "search",
            "engine",
            "index",
            "search",
        ],  # => "search" appears TWICE -- the highest-tf doc
        1: ["search", "results"],  # => doc 1's tokens, this fixture's row
        2: ["index", "documents"],  # => doc 2's tokens, this fixture's row
    }  # => opens/closes this multi-line literal
    ranking: list[tuple[int, float]] = rank_by_tfidf(
        docs, ["search"]
    )  # => co-14: ranked by summed tf-idf
    for doc_id, score in ranking:  # => iterates one item at a time
        print(f"doc {doc_id}: score={score:.4f}")  # => shows doc

    n_docs: int = len(docs)  # => this fixture's own size
    df_search: int = 2  # => "search" appears in docs 0 and 1
    hand_top_score: float = 2 * math.log(
        n_docs / df_search
    )  # => doc 0's tf=2 for "search"
    assert ranking[0] == (0, ranking[0][1]), (
        "doc 0 must rank first -- it has the highest tf for 'search'"
    )  # => doc 0 must rank first -- it has the highest tf for 'search'
    assert abs(ranking[0][1] - hand_top_score) < 1e-9, (
        "the top score must match the hand computation"
    )  # => the top score must match the hand computation
    print(
        f"MATCH: doc 0 ranks first with score {ranking[0][1]:.4f}, equal to the hand-computed {hand_top_score:.4f}"
    )  # => shows MATCH: doc 0 ranks first with score


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end

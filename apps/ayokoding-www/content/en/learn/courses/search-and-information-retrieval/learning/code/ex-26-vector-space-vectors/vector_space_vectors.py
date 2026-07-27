# pyright: strict
"""Example 26: Vector-Space Vectors (co-15)."""

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


def as_tfidf_vector(
    tokens: list[str], df: dict[str, int], n_docs: int
) -> dict[
    str, float
]:  # => represent one document as a sparse tf-idf vector: term -> weight
    """Represent one document as a sparse tf-idf vector: term -> weight."""
    tf: dict[str, int] = term_frequency(tokens)  # => tf = term_frequency(tokens)
    return {
        term: count * math.log(n_docs / df[term]) for term, count in tf.items()
    }  # => co-15: one dim per term


def main() -> None:  # => defines main
    docs: dict[int, list[str]] = {  # => docs = {
        0: ["search", "engine", "index"],  # => doc 0's tokens, this fixture's row
        1: ["search", "results", "fast"],  # => doc 1's tokens, this fixture's row
    }  # => opens/closes this multi-line literal
    n_docs: int = len(docs)  # => this fixture's own size
    df: dict[str, int] = document_frequency(docs)  # => df = document_frequency(docs)
    vec0: dict[str, float] = as_tfidf_vector(
        docs[0], df, n_docs
    )  # => co-15: doc 0 as a sparse vector
    vec1: dict[str, float] = as_tfidf_vector(
        docs[1], df, n_docs
    )  # => co-15: doc 1 as a sparse vector
    print(
        f"vec0 (doc 0): {dict((t, round(w, 4)) for t, w in vec0.items())}"
    )  # => shows vec0 (doc 0)
    print(
        f"vec1 (doc 1): {dict((t, round(w, 4)) for t, w in vec1.items())}"
    )  # => shows vec1 (doc 1)

    shared_terms: set[str] = set(vec0) & set(
        vec1
    )  # => terms both documents actually share
    print(f"shared terms: {sorted(shared_terms)}")  # => shows shared terms

    assert "search" in vec0 and "search" in vec1, (
        "'search' must appear as a dimension in BOTH vectors"
    )  # => 'search' must appear as a dimension in BOTH vectors
    assert shared_terms == {"search"}, (
        "'search' must be the ONLY term shared between these two documents"
    )  # => 'search' must be the ONLY term shared between these two documents
    print(
        f"MATCH: 'search' appears in both vectors, and is the exactly-one shared dimension between them"
    )  # => shows MATCH: 'search' appears in both vectors, and is the exactly-one shared dimension between them


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end

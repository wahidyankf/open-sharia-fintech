# pyright: strict
"""Example 14: TF-IDF Weight (co-14)."""

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


def tf_idf_matrix(
    docs: dict[int, list[str]],
) -> dict[
    int, dict[str, float]
]:  # => compute tf-idf for every (term, doc) pair: weight = tf * log(N / df)
    """Compute tf-idf for every (term, doc) pair: weight = tf * log(N / df)."""
    n_docs: int = len(docs)  # => N -- needed by every idf() call below
    df: dict[str, int] = document_frequency(
        docs
    )  # => co-13: corpus-wide document frequencies
    matrix: dict[
        int, dict[str, float]
    ] = {}  # => co-14: doc_id -> {term: tf-idf weight}
    for doc_id, tokens in docs.items():  # => iterates one item at a time
        tf: dict[str, int] = term_frequency(
            tokens
        )  # => co-12: this doc's own term frequencies
        matrix[doc_id] = {
            term: count * math.log(n_docs / df[term]) for term, count in tf.items()
        }  # => co-14: tf * idf
    return matrix  # => returns matrix


def main() -> None:  # => defines main
    docs: dict[
        int, list[str]
    ] = {  # => a tiny 3-doc fixture, hand-verifiable; "index" is in ALL 3 docs on purpose
        0: [
            "search",
            "engine",
            "search",
            "index",
        ],  # => doc 0's tokens, this fixture's row
        1: ["search", "index"],  # => doc 1's tokens, this fixture's row
        2: ["index", "index", "fast"],  # => doc 2's tokens, this fixture's row
    }  # => opens/closes this multi-line literal
    matrix: dict[int, dict[str, float]] = tf_idf_matrix(
        docs
    )  # => co-14: the full tf-idf weight matrix
    for doc_id in sorted(matrix):  # => iterates one item at a time
        weights: dict[str, float] = matrix[doc_id]  # => weights = matrix[doc_id]
        print(
            f"doc {doc_id}: "
            + ", ".join(f"{t}={w:.4f}" for t, w in sorted(weights.items()))
        )  # => shows doc

    n_docs: int = len(docs)  # => this fixture's own size
    hand_weight_search_doc0: float = 2 * math.log(
        n_docs / 2
    )  # => tf("search", doc0)=2, df("search")=2
    assert math.isclose(matrix[0]["search"], hand_weight_search_doc0, abs_tol=1e-9), (
        "doc 0's 'search' weight must match the hand computation tf=2 * log(3/2)"
    )  # => doc 0's 'search' weight must match the hand computation tf=2 * log(3/2)
    hand_weight_index_doc2: float = 2 * math.log(
        n_docs / 3
    )  # => tf("index", doc2)=2, df("index")=3 (present in ALL docs)
    assert math.isclose(matrix[2]["index"], hand_weight_index_doc2, abs_tol=1e-9), (
        "doc 2's 'index' weight must be 0 -- 'index' appears in all 3 docs, so idf('index') == 0"
    )  # => doc 2's 'index' weight must be 0 -- 'index' appears in all 3 docs, so idf('index') == 0
    print(
        "MATCH: the computed tf-idf matrix equals the hand-derived weights for 'search' in doc 0 and 'index' in doc 2"
    )  # => shows MATCH: the computed tf-idf matrix equals the hand-derived weights for 'search' in doc 0 and 'index' in doc 2


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end

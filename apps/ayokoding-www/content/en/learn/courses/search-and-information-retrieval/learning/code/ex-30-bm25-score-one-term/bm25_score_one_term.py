# pyright: strict
"""Example 30: BM25 Score: One Term (co-16)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import math  # => stdlib math -- log/sqrt for idf, cosine, and skip-pointer spacing


def bm25_idf(
    term_df: int, n_docs: int
) -> float:  # => bM25's own RSJ idf: log((N - df + 0.5) / (df + 0.5)) -- distinct from plain log(N/df)
    """BM25's own RSJ idf: log((N - df + 0.5) / (df + 0.5)) -- distinct from plain log(N/df)."""
    return math.log(
        (n_docs - term_df + 0.5) / (term_df + 0.5)
    )  # => returns math.log((n_docs - term_df + 0.5) / (term_df + 0.5))


def bm25_term_weight(  # => defines bm25 term weight
    tf: int,
    term_df: int,
    n_docs: int,
    dl: float,
    avgdl: float,
    *,
    k1: float = 1.2,
    b: float = 0.75,  # => part of this step's computation, continued from the line above
) -> float:  # => part of this step's computation, continued from the line above
    """One query term's BM25 contribution: RSJ idf * saturating tf * length normalization."""
    idf: float = bm25_idf(term_df, n_docs)  # => idf = bm25_idf(term_df, n_docs)
    length_norm: float = (1 - b) + b * (
        dl / avgdl
    )  # => co-18: B -- 1.0 at average length, >1 for long docs
    return (
        idf * (tf * (k1 + 1)) / (tf + k1 * length_norm)
    )  # => co-17: the k1-saturated, B-normalized term score


def bm25_score(  # => defines bm25 score
    query_terms: list[
        str
    ],  # => part of this step's computation, continued from the line above
    doc_tf: dict[
        str, int
    ],  # => part of this step's computation, continued from the line above
    df: dict[
        str, int
    ],  # => part of this step's computation, continued from the line above
    n_docs: int,  # => part of this step's computation, continued from the line above
    dl: float,  # => part of this step's computation, continued from the line above
    avgdl: float,  # => part of this step's computation, continued from the line above
    *,  # => part of this step's computation, continued from the line above
    k1: float = 1.2,  # => k1 = 1.2,
    b: float = 0.75,  # => b = 0.75,
) -> float:  # => part of this step's computation, continued from the line above
    """Sum bm25_term_weight over every query term the document actually contains."""
    total: float = 0.0  # => total = 0.0
    for term in query_terms:  # => iterates one item at a time
        if term in doc_tf:  # => true when term in doc_tf
            total += bm25_term_weight(
                doc_tf[term], df.get(term, 0), n_docs, dl, avgdl, k1=k1, b=b
            )  # => part of this step's computation, continued from the line above
    return total  # => returns total


def main() -> None:  # => defines main
    tf, term_df, n_docs = (
        3,
        2,
        5,
    )  # => this term occurs 3 times in the doc; 2 of 5 docs contain it
    dl, avgdl = 10.0, 8.0  # => this doc has 10 tokens; the corpus average is 8
    k1, b = 1.2, 0.75  # => co-19: the Lucene/Elasticsearch software defaults

    weight: float = bm25_term_weight(
        tf, term_df, n_docs, dl, avgdl, k1=k1, b=b
    )  # => co-16: the function under test
    print(
        f"bm25_term_weight(tf={tf}, df={term_df}, N={n_docs}, dl={dl}, avgdl={avgdl}) = {weight:.6f}"
    )  # => shows bm25_term_weight(tf=

    # Hand computation, written out independently (not calling bm25_term_weight):
    hand_idf: float = math.log(
        (n_docs - term_df + 0.5) / (term_df + 0.5)
    )  # => hand idf = math.log((n_docs - term_df + 0.5) / (term_df + ...
    hand_B: float = (1 - b) + b * (dl / avgdl)  # => hand B = (1 - b) + b * (dl / avgdl)
    hand_weight: float = (
        hand_idf * (tf * (k1 + 1)) / (tf + k1 * hand_B)
    )  # => hand weight = hand_idf * (tf * (k1 + 1)) / (tf + k1 * hand_B)
    print(
        f"hand computation: idf={hand_idf:.6f} B={hand_B:.6f} weight={hand_weight:.6f}"
    )  # => shows hand computation: idf=

    assert math.isclose(weight, hand_weight, rel_tol=1e-9), (
        "bm25_term_weight must match the independent hand computation"
    )  # => bm25_term_weight must match the independent hand computation
    print(
        f"MATCH: bm25_term_weight's {weight:.6f} equals the hand computation's {hand_weight:.6f}"
    )  # => shows MATCH: bm25_term_weight's


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end

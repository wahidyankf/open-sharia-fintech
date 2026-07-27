# pyright: strict
"""Example 35: BM25 k1 Sweep (co-17)."""

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


def marginal_gain(
    term_df: int,
    n_docs: int,
    dl: float,
    avgdl: float,
    k1: float,
    tf_from: int,
    tf_to: int,
) -> (
    float
):  # => the score gained by moving from tf_from to tf_to occurrences, at a fixed k1
    """The score gained by moving from tf_from to tf_to occurrences, at a fixed k1."""
    return bm25_term_weight(
        tf_to, term_df, n_docs, dl, avgdl, k1=k1
    ) - bm25_term_weight(
        tf_from, term_df, n_docs, dl, avgdl, k1=k1
    )  # => returns bm25_term_weight(tf_to, term_df, n_docs, dl, avgdl, k1=k1...


def main() -> None:  # => defines main
    term_df, n_docs = (
        3,
        10,
    )  # => part of this step's computation, continued from the line above
    dl, avgdl = 8.0, 8.0  # => neutral length normalization

    for k1 in (0.5, 1.2, 2.0, 5.0):  # => co-17: small to large saturation constants
        early_gain: float = marginal_gain(
            term_df, n_docs, dl, avgdl, k1, 1, 2
        )  # => gain from the FIRST extra occurrence
        late_gain: float = marginal_gain(
            term_df, n_docs, dl, avgdl, k1, 9, 10
        )  # => gain from a MUCH later occurrence
        print(
            f"k1={k1:.1f}: early gain (tf 1->2)={early_gain:.4f}  late gain (tf 9->10)={late_gain:.4f}"
        )  # => shows k1=

    low_k1_late_gain: float = marginal_gain(
        term_df, n_docs, dl, avgdl, 0.5, 9, 10
    )  # => a SMALL k1's late-stage gain
    high_k1_late_gain: float = marginal_gain(
        term_df, n_docs, dl, avgdl, 5.0, 9, 10
    )  # => a LARGE k1's late-stage gain
    assert high_k1_late_gain > low_k1_late_gain, (
        "a LARGER k1 must still yield a bigger late-stage marginal gain (saturates later)"
    )  # => a LARGER k1 must still yield a bigger late-stage marginal gain (saturates later)
    print(
        f"MATCH: at tf 9->10, k1=5.0's gain ({high_k1_late_gain:.4f}) exceeds k1=0.5's gain ({low_k1_late_gain:.4f}) -- k1 moves the saturation point"
    )  # => shows MATCH: at tf 9->10, k1=5.0's gain (


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end

# pyright: strict
"""Example 34: BM25 b Sweep (co-18)."""

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
    term_df, n_docs = (
        3,
        10,
    )  # => part of this step's computation, continued from the line above
    avgdl: float = (
        20.0  # => the corpus average -- short doc is well below it, long doc well above
    )

    short_dl, short_tf = (
        5.0,
        2,
    )  # => a SHORT, concentrated document: few words, term appears twice
    long_dl, long_tf = (
        50.0,
        4,
    )  # => a LONG, diluted document: many words, term appears more often in raw count

    for b in (
        0.0,
        0.5,
        0.75,
        1.0,
    ):  # => co-18: sweeping the length-normalization strength
        short_score: float = bm25_term_weight(
            short_tf, term_df, n_docs, short_dl, avgdl, b=b
        )  # => short score = bm25_term_weight(short_tf, term_df, n_docs, sho...
        long_score: float = bm25_term_weight(
            long_tf, term_df, n_docs, long_dl, avgdl, b=b
        )  # => long score = bm25_term_weight(long_tf, term_df, n_docs, long...
        winner: str = (
            "short" if short_score > long_score else "long"
        )  # => winner = "short" if short_score > long_score else "long"
        print(
            f"b={b:.2f}: short={short_score:.4f}  long={long_score:.4f}  winner={winner}"
        )  # => shows b=

    score_at_b0_short: float = bm25_term_weight(
        short_tf, term_df, n_docs, short_dl, avgdl, b=0.0
    )  # => score at b0 short = bm25_term_weight(short_tf, term_df, n_docs, sho...
    score_at_b0_long: float = bm25_term_weight(
        long_tf, term_df, n_docs, long_dl, avgdl, b=0.0
    )  # => score at b0 long = bm25_term_weight(long_tf, term_df, n_docs, long...
    score_at_b1_short: float = bm25_term_weight(
        short_tf, term_df, n_docs, short_dl, avgdl, b=1.0
    )  # => score at b1 short = bm25_term_weight(short_tf, term_df, n_docs, sho...
    score_at_b1_long: float = bm25_term_weight(
        long_tf, term_df, n_docs, long_dl, avgdl, b=1.0
    )  # => score at b1 long = bm25_term_weight(long_tf, term_df, n_docs, long...

    assert score_at_b0_long > score_at_b0_short, (
        "at b=0 (no length norm), the long doc's higher raw tf must win"
    )  # => at b=0 (no length norm), the long doc's higher raw tf must win
    assert score_at_b1_short > score_at_b1_long, (
        "at b=1 (full length norm), the short doc must overtake the long one"
    )  # => at b=1 (full length norm), the short doc must overtake the long one
    print(
        "MATCH: the ranking genuinely flips -- long doc wins at b=0, short doc wins at b=1"
    )  # => shows MATCH: the ranking genuinely flips -- long doc wins at b=0, short doc wins at b=1


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end

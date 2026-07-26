# pyright: strict
"""Example 32: TF-IDF vs BM25 Saturation (co-17)."""

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


def tfidf_score(
    tf: int, term_df: int, n_docs: int
) -> float:  # => plain tf-idf: tf * log(N / df) -- LINEAR in tf, no saturation
    """Plain tf-idf: tf * log(N / df) -- LINEAR in tf, no saturation."""
    return tf * math.log(n_docs / term_df)  # => returns tf * math.log(n_docs / term_df)


def main() -> None:  # => defines main
    term_df, n_docs = (
        3,
        10,
    )  # => part of this step's computation, continued from the line above
    dl, avgdl = 8.0, 8.0  # => neutral length normalization, isolating the tf effect

    tfidf_scores: list[float] = [
        tfidf_score(tf, term_df, n_docs) for tf in (10, 20, 40, 80)
    ]  # => co-14: linear growth
    bm25_scores: list[float] = [
        bm25_term_weight(tf, term_df, n_docs, dl, avgdl) for tf in (10, 20, 40, 80)
    ]  # => co-17: saturating growth
    for tf, ts, bs in zip(
        (10, 20, 40, 80), tfidf_scores, bm25_scores
    ):  # => iterates one item at a time
        print(f"tf={tf:>3}: tf-idf={ts:8.4f}   bm25={bs:6.4f}")  # => shows tf=

    tfidf_growth_10_to_80: float = (
        tfidf_scores[-1] - tfidf_scores[0]
    )  # => tf-idf's growth over the SAME tf range
    bm25_growth_10_to_80: float = (
        bm25_scores[-1] - bm25_scores[0]
    )  # => BM25's growth over the SAME tf range
    print(
        f"growth from tf=10 to tf=80: tf-idf grew by {tfidf_growth_10_to_80:.4f}, bm25 grew by {bm25_growth_10_to_80:.4f}"
    )  # => shows growth from tf=10 to tf=80: tf-idf grew by

    assert tfidf_growth_10_to_80 > bm25_growth_10_to_80 * 5, (
        "tf-idf's growth must vastly outpace BM25's over a wide tf range"
    )  # => tf-idf's growth must vastly outpace BM25's over a wide tf range
    assert bm25_scores[-1] < bm25_scores[0] * 1.5, (
        "BM25 must be near-flat by tf=80, having started saturating much earlier"
    )  # => BM25 must be near-flat by tf=80, having started saturating much earlier
    print(
        "MATCH: tf-idf keeps climbing near-linearly while BM25 has essentially flattened out over the same range"
    )  # => shows MATCH: tf-idf keeps climbing near-linearly while BM25 has essentially flattened out over the same range


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end

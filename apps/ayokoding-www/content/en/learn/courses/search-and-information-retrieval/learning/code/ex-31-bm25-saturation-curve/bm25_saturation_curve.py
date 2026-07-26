# pyright: strict
"""Example 31: BM25 Saturation Curve (co-17)."""

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
    term_df, n_docs = 3, 10  # => a moderately common term
    dl, avgdl = (
        8.0,
        8.0,
    )  # => dl == avgdl -- length normalization is neutral (B == 1), isolating tf's effect
    k1: float = 1.2  # => the Lucene/Elasticsearch default

    scores: list[float] = [
        bm25_term_weight(tf, term_df, n_docs, dl, avgdl, k1=k1) for tf in range(1, 21)
    ]  # => co-17: score at each tf
    deltas: list[float] = [
        scores[i] - scores[i - 1] for i in range(1, len(scores))
    ]  # => the marginal gain of EACH extra occurrence
    for tf, score in zip(range(1, 21), scores):  # => iterates one item at a time
        marker: str = (
            f" (+{scores[tf - 1] - scores[tf - 2]:.4f})" if tf > 1 else ""
        )  # => marker = f" (+{scores[tf - 1] - scores[tf - 2]:.4f})" if...
        print(f"tf={tf:>2}: score={score:.4f}{marker}")  # => shows tf=

    for i in range(1, len(deltas)):  # => every adjacent PAIR of marginal gains
        assert deltas[i] <= deltas[i - 1] + 1e-9, (
            f"marginal gain must be non-increasing (tf={i + 2})"
        )  # => marginal gain must be non-increasing (tf={i + 2})
    assert deltas[0] > deltas[-1], (
        "the FIRST extra occurrence must help strictly more than the LAST one shown"
    )  # => the FIRST extra occurrence must help strictly more than the LAST one shown
    print(
        f"MATCH: marginal gain shrinks monotonically from {deltas[0]:.4f} (tf 1->2) to {deltas[-1]:.4f} (tf 19->20)"
    )  # => shows MATCH: marginal gain shrinks monotonically from


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end

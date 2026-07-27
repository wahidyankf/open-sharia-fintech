# pyright: strict
"""Example 33: BM25 Length Normalization (co-18)."""

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
    avgdl: float = 20.0  # => the corpus average document length
    tf: int = 4  # => the SAME term count in both documents below

    short_doc_len: float = 10.0  # => half the average length
    long_doc_len: float = 60.0  # => three times the average length

    short_score: float = bm25_term_weight(
        tf, term_df, n_docs, short_doc_len, avgdl
    )  # => co-18: short doc, same tf
    long_score: float = bm25_term_weight(
        tf, term_df, n_docs, long_doc_len, avgdl
    )  # => co-18: long doc, same tf
    print(
        f"short doc (dl={short_doc_len}, tf={tf}): score={short_score:.4f}"
    )  # => shows short doc (dl=
    print(
        f"long doc  (dl={long_doc_len}, tf={tf}): score={long_score:.4f}"
    )  # => shows long doc  (dl=

    b: float = 0.75  # => the default b
    short_B: float = (1 - b) + b * (
        short_doc_len / avgdl
    )  # => short B = (1 - b) + b * (short_doc_len / avgdl)
    long_B: float = (1 - b) + b * (
        long_doc_len / avgdl
    )  # => long B = (1 - b) + b * (long_doc_len / avgdl)
    print(f"B(short)={short_B:.4f}  B(long)={long_B:.4f}")  # => shows B(short)=

    assert long_B > short_B, (
        "the longer document must have a LARGER B (length-norm factor)"
    )  # => the longer document must have a LARGER B (length-norm factor)
    assert short_score > long_score, (
        "with EQUAL tf, the SHORTER document must score HIGHER"
    )  # => with EQUAL tf, the SHORTER document must score HIGHER
    print(
        f"MATCH: with identical tf={tf}, the short doc (B={short_B:.4f}) outscores the long doc (B={long_B:.4f})"
    )  # => shows MATCH: with identical tf=


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end

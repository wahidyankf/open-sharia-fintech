# pyright: strict
"""Example 36: BM25 Defaults (co-19)."""

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
    default_k1: float = 1.2  # => co-19: the Lucene/Elasticsearch SOFTWARE default
    default_b: float = 0.75  # => co-19: the Lucene/Elasticsearch SOFTWARE default

    paper_k1_lower, paper_k1_upper = (
        1.2,
        2.0,
    )  # => Robertson & Zaragoza (2009)'s own recommended OPEN interval
    paper_b_lower, paper_b_upper = (
        0.5,
        0.8,
    )  # => Robertson & Zaragoza (2009)'s own recommended OPEN interval

    k1_in_papers_open_range: bool = (
        paper_k1_lower < default_k1 < paper_k1_upper
    )  # => STRICT inequality, as the paper states it
    b_in_papers_open_range: bool = (
        paper_b_lower < default_b < paper_b_upper
    )  # => STRICT inequality, as the paper states it
    print(
        f"default k1={default_k1}: inside paper's OPEN range (1.2, 2.0)? {k1_in_papers_open_range}"
    )  # => shows default k1=
    print(
        f"default b={default_b}: inside paper's OPEN range (0.5, 0.8)? {b_in_papers_open_range}"
    )  # => shows default b=

    term_df, n_docs, dl, avgdl, tf = (
        3,
        10,
        8.0,
        8.0,
        4,
    )  # => part of this step's computation, continued from the line above
    score: float = bm25_term_weight(
        tf, term_df, n_docs, dl, avgdl, k1=default_k1, b=default_b
    )  # => the software defaults, applied
    print(
        f"score with software defaults (k1={default_k1}, b={default_b}): {score:.4f}"
    )  # => shows score with software defaults (k1=

    assert not k1_in_papers_open_range, (
        "k1=1.2 sits exactly ON the paper's lower boundary -- NOT strictly inside its open interval"
    )  # => k1=1.2 sits exactly ON the paper's lower boundary -- NOT strictly inside its open interval
    assert b_in_papers_open_range, (
        "b=0.75 DOES sit strictly inside the paper's own recommended (0.5, 0.8) range"
    )  # => b=0.75 DOES sit strictly inside the paper's own recommended (0.5, 0.8) range
    print(
        "MATCH: k1=1.2 is the boundary value (not strictly inside the paper's range), while b=0.75 is strictly inside it"
    )  # => shows MATCH: k1=1.2 is the boundary value (not strictly inside the paper's range), while b=0.75 is strictly inside it


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end

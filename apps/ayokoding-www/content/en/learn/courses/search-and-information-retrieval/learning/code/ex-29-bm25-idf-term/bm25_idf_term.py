# pyright: strict
"""Example 29: BM25 IDF Term (co-16)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import math  # => stdlib math -- log/sqrt for idf, cosine, and skip-pointer spacing


def bm25_idf(
    term_df: int, n_docs: int
) -> float:  # => bM25's own RSJ idf: log((N - df + 0.5) / (df + 0.5))
    """BM25's own RSJ idf: log((N - df + 0.5) / (df + 0.5))."""
    return math.log(
        (n_docs - term_df + 0.5) / (term_df + 0.5)
    )  # => co-16: Robertson & Zaragoza (2009) eq. 3.3


def plain_idf(
    term_df: int, n_docs: int
) -> float:  # => the Example 13 tf-idf idf, for comparison: log(N / df)
    """The Example 13 tf-idf idf, for comparison: log(N / df)."""
    return math.log(n_docs / term_df)  # => returns math.log(n_docs / term_df)


def main() -> None:  # => defines main
    n_docs: int = 10  # => a small corpus, N
    common_df: int = 10  # => a term present in EVERY document
    rare_df: int = 1  # => a term present in only one document

    bm25_common: float = bm25_idf(
        common_df, n_docs
    )  # => co-16: BM25's idf for the ubiquitous term
    plain_common: float = plain_idf(
        common_df, n_docs
    )  # => the plain tf-idf idf for the same term
    print(
        f"term in ALL {n_docs} docs: bm25_idf={bm25_common:.4f}  plain_idf={plain_common:.4f}"
    )  # => shows term in ALL

    bm25_rare: float = bm25_idf(
        rare_df, n_docs
    )  # => bm25 rare = bm25_idf(rare_df, n_docs)
    plain_rare: float = plain_idf(
        rare_df, n_docs
    )  # => plain rare = plain_idf(rare_df, n_docs)
    print(
        f"term in only 1 doc:   bm25_idf={bm25_rare:.4f}  plain_idf={plain_rare:.4f}"
    )  # => shows term in only 1 doc:   bm25_idf=

    assert math.isfinite(bm25_common), (
        "BM25's idf must stay FINITE even for a term in every document"
    )  # => BM25's idf must stay FINITE even for a term in every document
    assert bm25_common < 0, (
        "BM25's idf for a term in EVERY doc goes NEGATIVE, unlike plain idf's 0"
    )  # => BM25's idf for a term in EVERY doc goes NEGATIVE, unlike plain idf's 0
    assert not math.isclose(bm25_common, plain_common), (
        "BM25's idf and plain idf must be DIFFERENT formulas"
    )  # => BM25's idf and plain idf must be DIFFERENT formulas
    print(
        f"MATCH: bm25_idf({common_df}/{n_docs})={bm25_common:.4f} is finite and negative, unlike plain_idf's {plain_common:.4f}"
    )  # => shows MATCH: bm25_idf(


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end

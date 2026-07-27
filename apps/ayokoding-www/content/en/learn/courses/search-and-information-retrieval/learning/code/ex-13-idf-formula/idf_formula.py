# pyright: strict
"""Example 13: IDF Formula (co-13)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import math  # => stdlib math -- log/sqrt for idf, cosine, and skip-pointer spacing


def idf(
    term_df: int, n_docs: int
) -> float:  # => inverse document frequency: idf = log(N / df) (IR-book form)
    """Inverse document frequency: idf = log(N / df) (IR-book form)."""
    return math.log(n_docs / term_df)  # => co-13: rarer term (small df) -> larger idf


def main() -> None:  # => defines main
    n_docs: int = 1_000  # => corpus size N
    common_df: int = 900  # => "the" -- appears in almost every document
    rare_df: int = 5  # => "quasar" -- appears in almost none

    common_idf: float = idf(common_df, n_docs)  # => a near-ubiquitous term
    rare_idf: float = idf(rare_df, n_docs)  # => a genuinely rare term
    print(
        f"idf('the',    df={common_df:>4}/{n_docs}) = {common_idf:.4f}"
    )  # => shows idf('the',    df=
    print(
        f"idf('quasar', df={rare_df:>4}/{n_docs}) = {rare_idf:.4f}"
    )  # => shows idf('quasar', df=

    all_docs_idf: float = idf(n_docs, n_docs)  # => a term present in EVERY document
    print(
        f"idf(term in every doc, df={n_docs}/{n_docs}) = {all_docs_idf:.4f}"
    )  # => shows idf(term in every doc, df=

    assert rare_idf > common_idf, (
        "a rarer term (lower df) must have a LARGER idf"
    )  # => a rarer term (lower df) must have a LARGER idf
    assert math.isclose(all_docs_idf, 0.0, abs_tol=1e-9), (
        "a term in every doc must have idf == 0"
    )  # => a term in every doc must have idf == 0
    print(
        f"MATCH: rare_idf ({rare_idf:.4f}) exceeds common_idf ({common_idf:.4f}), and a ubiquitous term scores idf=0"
    )  # => shows MATCH: rare_idf (


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end

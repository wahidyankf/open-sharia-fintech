# pyright: strict
"""Example 65: BM25F: Fields (co-31)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import math  # => stdlib math -- log/sqrt for idf, cosine, and skip-pointer spacing


def bm25f_score(  # => defines bm25f score
    tf_by_field: dict[str, int],
    field_weights: dict[str, float],
    term_df: int,
    n_docs: int,
    k1: float = 1.2,  # => part of this step's computation, continued from the line above
) -> float:  # => part of this step's computation, continued from the line above
    """BM25F: combine WEIGHTED tf across fields FIRST, saturate ONCE on the combined total."""
    weighted_tf: float = sum(
        tf_by_field.get(field, 0) * field_weights[field] for field in field_weights
    )  # => co-31: combine-first
    idf: float = math.log(
        (n_docs - term_df + 0.5) / (term_df + 0.5)
    )  # => co-16: the SAME RSJ idf, applied once
    return (
        idf * (weighted_tf * (k1 + 1)) / (weighted_tf + k1)
    )  # => co-31: ONE saturation curve over the combined tf


def main() -> None:  # => defines main
    field_weights: dict[str, float] = {
        "title": 3.0,
        "body": 1.0,
    }  # => co-31: title matches count 3x as much as body matches
    term_df, n_docs = (
        3,
        10,
    )  # => part of this step's computation, continued from the line above

    title_match: dict[str, int] = {
        "title": 1,
        "body": 0,
    }  # => the term appears ONCE, in the title only
    body_match: dict[str, int] = {
        "title": 0,
        "body": 1,
    }  # => the term appears ONCE, in the body only (equal RAW tf)

    title_score: float = bm25f_score(
        title_match, field_weights, term_df, n_docs
    )  # => co-31: weighted by title's 3.0
    body_score: float = bm25f_score(
        body_match, field_weights, term_df, n_docs
    )  # => co-31: weighted by body's 1.0
    print(
        f"title match (raw tf=1): score={title_score:.4f}"
    )  # => shows title match (raw tf=1): score=
    print(
        f"body match  (raw tf=1): score={body_score:.4f}"
    )  # => shows body match  (raw tf=1): score=

    assert title_score > body_score, (
        "with EQUAL raw tf, the TITLE match must outrank the body match (higher field weight)"
    )  # => with EQUAL raw tf, the TITLE match must outrank the body match (higher field weight)
    print(
        f"MATCH: an equal-tf title match ({title_score:.4f}) outranks the body match ({body_score:.4f}) due to field weighting"
    )  # => shows MATCH: an equal-tf title match (


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end

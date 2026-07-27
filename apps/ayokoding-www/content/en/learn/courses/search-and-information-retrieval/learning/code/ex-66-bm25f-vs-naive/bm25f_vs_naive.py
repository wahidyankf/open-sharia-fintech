# pyright: strict
"""Example 66: BM25F vs Naive (co-31)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import math  # => stdlib math -- log/sqrt for idf, cosine, and skip-pointer spacing


def bm25f_combine_first(
    tf_by_field: dict[str, int],
    field_weights: dict[str, float],
    term_df: int,
    n_docs: int,
    k1: float = 1.2,
) -> float:  # => the CORRECT BM25F: sum weighted tf across fields, saturate ONCE
    """The CORRECT BM25F: sum weighted tf across fields, saturate ONCE."""
    weighted_tf: float = sum(
        tf_by_field.get(field, 0) * field_weights[field] for field in field_weights
    )  # => weighted tf = sum(tf_by_field.get(field, 0) * field_weights[f...
    idf: float = math.log(
        (n_docs - term_df + 0.5) / (term_df + 0.5)
    )  # => idf = math.log((n_docs - term_df + 0.5) / (term_df + ...
    return (
        idf * (weighted_tf * (k1 + 1)) / (weighted_tf + k1)
    )  # => returns idf * (weighted_tf * (k1 + 1)) / (weighted_tf + k1)


def naive_saturate_then_sum(
    tf_by_field: dict[str, int],
    field_weights: dict[str, float],
    term_df: int,
    n_docs: int,
    k1: float = 1.2,
) -> float:  # => the BROKEN naive approach: saturate EACH field's weighted tf separately, then add
    """The BROKEN naive approach: saturate EACH field's weighted tf separately, then add."""
    idf: float = math.log(
        (n_docs - term_df + 0.5) / (term_df + 0.5)
    )  # => idf = math.log((n_docs - term_df + 0.5) / (term_df + ...
    total: float = 0.0  # => total = 0.0
    for (
        field,
        weight,
    ) in field_weights.items():  # => co-31: saturates PER FIELD -- the bug
        weighted_tf_field: float = (
            tf_by_field.get(field, 0) * weight
        )  # => weighted tf field = tf_by_field.get(field, 0) * weight
        if weighted_tf_field > 0:  # => true when weighted_tf_field > 0
            total += (
                idf * (weighted_tf_field * (k1 + 1)) / (weighted_tf_field + k1)
            )  # => part of this step's computation, continued from the line above
    return total  # => returns total


def main() -> None:  # => defines main
    field_weights: dict[str, float] = {
        "title": 1.0,
        "body": 1.0,
    }  # => EQUAL weights, isolating the combine-order effect
    term_df, n_docs = (
        3,
        10,
    )  # => part of this step's computation, continued from the line above

    all_in_one_field: dict[str, int] = {
        "title": 10,
        "body": 0,
    }  # => tf=10, ALL in one field
    split_evenly: dict[str, int] = {
        "title": 5,
        "body": 5,
    }  # => the SAME total tf=10, split 5+5 across two fields

    combine_first_one: float = bm25f_combine_first(
        all_in_one_field, field_weights, term_df, n_docs
    )  # => co-31: correct BM25F
    combine_first_split: float = bm25f_combine_first(
        split_evenly, field_weights, term_df, n_docs
    )  # => combine first split = bm25f_combine_first(split_evenly, field_weights...
    naive_one: float = naive_saturate_then_sum(
        all_in_one_field, field_weights, term_df, n_docs
    )  # => the BROKEN naive version
    naive_split: float = naive_saturate_then_sum(
        split_evenly, field_weights, term_df, n_docs
    )  # => naive split = naive_saturate_then_sum(split_evenly, field_wei...
    print(
        f"combine-first: all-in-one={combine_first_one:.4f}  split={combine_first_split:.4f}"
    )  # => shows combine-first: all-in-one=
    print(
        f"naive:         all-in-one={naive_one:.4f}  split={naive_split:.4f}"
    )  # => shows naive:         all-in-one=

    assert math.isclose(combine_first_one, combine_first_split, rel_tol=1e-9), (
        "combine-first must give the SAME score regardless of split -- only total tf matters"
    )  # => combine-first must give the SAME score regardless of split -- only total tf matters
    assert not math.isclose(naive_one, naive_split, rel_tol=1e-9), (
        "the naive version must DISAGREE across splits -- it breaks the invariant"
    )  # => the naive version must DISAGREE across splits -- it breaks the invariant
    assert naive_split > naive_one, (
        "splitting tf evenly must INFLATE the naive score, since saturation resets per field"
    )  # => splitting tf evenly must INFLATE the naive score, since saturation resets per field
    print(
        f"MATCH: combine-first is split-invariant ({combine_first_one:.4f} both ways); naive is NOT ({naive_one:.4f} vs {naive_split:.4f})"
    )  # => shows MATCH: combine-first is split-invariant (


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end

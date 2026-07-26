# pyright: strict
"""Example 42: F1 Harmonic Mean (co-21)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def f1_score(
    precision: float, recall: float
) -> float:  # => the harmonic mean of precision and recall
    """The harmonic mean of precision and recall."""
    if precision + recall == 0:  # => true when precision + recall == 0
        return 0.0  # => returns 0.0
    return (
        2 * precision * recall / (precision + recall)
    )  # => co-21: harmonic, NOT arithmetic, mean


def main() -> None:  # => defines main
    balanced_p, balanced_r = 0.8, 0.8  # => a BALANCED system
    lopsided_p, lopsided_r = (
        1.0,
        0.1,
    )  # => a LOPSIDED system -- perfect precision, terrible recall

    f1_balanced: float = f1_score(
        balanced_p, balanced_r
    )  # => f1 balanced = f1_score(balanced_p, balanced_r)
    f1_lopsided: float = f1_score(
        lopsided_p, lopsided_r
    )  # => f1 lopsided = f1_score(lopsided_p, lopsided_r)
    arithmetic_mean_lopsided: float = (
        lopsided_p + lopsided_r
    ) / 2  # => an arithmetic mean, for contrast
    print(
        f"balanced (p={balanced_p}, r={balanced_r}): F1={f1_balanced:.4f}"
    )  # => shows balanced (p=
    print(
        f"lopsided (p={lopsided_p}, r={lopsided_r}): F1={f1_lopsided:.4f}  (arithmetic mean would be {arithmetic_mean_lopsided:.4f})"
    )  # => shows lopsided (p=

    assert lopsided_r < f1_lopsided < arithmetic_mean_lopsided, (
        "F1 must sit BETWEEN recall and the arithmetic mean, closer to the SMALLER value"
    )  # => F1 must sit BETWEEN recall and the arithmetic mean, closer to the SMALLER value
    assert f1_lopsided < 0.2, (
        "F1 must stay near the smaller of the two lopsided values, not near their average"
    )  # => F1 must stay near the smaller of the two lopsided values, not near their average
    print(
        f"MATCH: F1={f1_lopsided:.4f} stays close to the smaller value (recall={lopsided_r}), far below the arithmetic mean {arithmetic_mean_lopsided:.4f}"
    )  # => shows MATCH: F1=


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end

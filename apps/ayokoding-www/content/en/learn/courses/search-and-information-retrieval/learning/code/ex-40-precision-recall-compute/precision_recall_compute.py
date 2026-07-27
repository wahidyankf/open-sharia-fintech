# pyright: strict
"""Example 40: Precision/Recall Compute (co-21)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def precision(
    retrieved: set[int], relevant: set[int]
) -> (
    float
):  # => |relevant ∩ retrieved| / |retrieved| -- denominator is what you RETURNED
    """|relevant ∩ retrieved| / |retrieved| -- denominator is what you RETURNED."""
    if not retrieved:  # => true when not retrieved
        return 0.0  # => returns 0.0
    return len(relevant & retrieved) / len(
        retrieved
    )  # => co-21: how much of what you returned was actually relevant


def recall(
    retrieved: set[int], relevant: set[int]
) -> (
    float
):  # => |relevant ∩ retrieved| / |relevant| -- denominator is what EXISTS to find
    """|relevant ∩ retrieved| / |relevant| -- denominator is what EXISTS to find."""
    if not relevant:  # => true when not relevant
        return 0.0  # => returns 0.0
    return len(relevant & retrieved) / len(
        relevant
    )  # => co-21: how much of what exists did you actually find


def main() -> None:  # => defines main
    relevant: set[int] = {
        1,
        2,
        3,
        4,
        5,
    }  # => the 5 documents that are ACTUALLY relevant to this query
    retrieved: set[int] = {
        1,
        2,
        6,
        7,
    }  # => the 4 documents the system actually returned

    p: float = precision(
        retrieved, relevant
    )  # => co-21: 2 of the 4 retrieved were relevant
    r: float = recall(retrieved, relevant)  # => co-21: 2 of the 5 relevant were found
    print(f"relevant: {sorted(relevant)}")  # => shows relevant
    print(f"retrieved: {sorted(retrieved)}")  # => shows retrieved
    print(f"precision: {p:.4f}  recall: {r:.4f}")  # => shows precision

    hand_precision: float = (
        2 / 4
    )  # => hand tally: {1,2} are the 2 relevant docs among the 4 retrieved
    hand_recall: float = (
        2 / 5
    )  # => hand tally: {1,2} are the 2 found docs among the 5 relevant
    assert p == hand_precision, (
        f"precision must equal the hand tally {hand_precision}"
    )  # => precision must equal the hand tally {hand_precision}
    assert r == hand_recall, (
        f"recall must equal the hand tally {hand_recall}"
    )  # => recall must equal the hand tally {hand_recall}
    print(
        f"MATCH: precision={p} and recall={r} both equal their hand-tallied values"
    )  # => shows MATCH: precision=


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end

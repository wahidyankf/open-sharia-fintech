# pyright: strict
"""Example 46: Average Precision (co-24)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def average_precision(
    ranked: list[int], relevant: set[int]
) -> float:  # => mean of precision@k, evaluated at every rank position where a relevant doc appears
    """Mean of precision@k, evaluated at every rank position where a relevant doc appears."""
    if not relevant:  # => true when not relevant
        return 0.0  # => returns 0.0
    precisions_at_hits: list[
        float
    ] = []  # => co-24: one precision@k value per relevant hit, in rank order
    hits_so_far: int = 0  # => a running counter, starting at zero
    for k, doc_id in enumerate(
        ranked, start=1
    ):  # => co-24: k is the 1-based rank position
        if doc_id in relevant:  # => true when doc_id in relevant
            hits_so_far += 1  # => advances hits_so_far
            precisions_at_hits.append(
                hits_so_far / k
            )  # => co-22: precision@k, evaluated ONLY at this hit
    return sum(precisions_at_hits) / len(
        relevant
    )  # => co-24: averaged over ALL relevant docs, not just the ones found


def main() -> None:  # => defines main
    relevant: set[int] = {2, 4, 6}  # => 3 truly relevant documents
    ranked: list[int] = [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
    ]  # => relevant docs land at ranks 2, 4, and 6

    ap: float = average_precision(
        ranked, relevant
    )  # => co-24: this query's own Average Precision
    print(f"ranked: {ranked}")  # => shows ranked
    print(f"relevant: {sorted(relevant)} (found at ranks 2, 4, 6)")  # => shows relevant
    print(f"average precision: {ap:.4f}")  # => shows average precision

    hand_p_at_2: float = 1 / 2  # => rank 2: 1 hit out of 2 seen so far
    hand_p_at_4: float = 2 / 4  # => rank 4: 2 hits out of 4 seen so far
    hand_p_at_6: float = 3 / 6  # => rank 6: 3 hits out of 6 seen so far
    hand_ap: float = (
        hand_p_at_2 + hand_p_at_4 + hand_p_at_6
    ) / 3  # => mean over the 3 relevant docs
    assert ap == hand_ap, (
        f"AP must equal the hand computation {hand_ap}"
    )  # => AP must equal the hand computation {hand_ap}
    print(
        f"MATCH: AP={ap} equals the hand computation ({hand_p_at_2}+{hand_p_at_4}+{hand_p_at_6})/3={hand_ap}"
    )  # => shows MATCH: AP=


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end

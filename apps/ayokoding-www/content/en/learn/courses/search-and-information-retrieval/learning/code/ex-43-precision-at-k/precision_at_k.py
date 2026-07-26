# pyright: strict
"""Example 43: Precision at K (co-22)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def precision_at_k(
    ranked_results: list[int], relevant: set[int], k: int
) -> float:  # => precision computed over only the top-k entries of a ranked result list
    """Precision computed over only the top-k entries of a ranked result list."""
    top_k: list[int] = ranked_results[:k]  # => co-22: only the FIRST k results count
    hits: int = sum(
        1 for doc_id in top_k if doc_id in relevant
    )  # => how many of the top k are relevant
    return hits / k if k > 0 else 0.0  # => returns hits / k if k > 0 else 0.0


def main() -> None:  # => defines main
    relevant: set[int] = {
        1,
        3,
        5,
        7,
        9,
        11,
        13,
    }  # => 7 truly relevant documents, corpus-wide
    ranked: list[int] = [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
    ]  # => the system's ranked output, best-first

    p_at_5: float = precision_at_k(
        ranked, relevant, k=5
    )  # => co-22: precision over just the top 5
    p_at_10: float = precision_at_k(
        ranked, relevant, k=10
    )  # => co-22: precision over the top 10
    print(f"ranked (top 10): {ranked}")  # => shows ranked (top 10)
    print(f"precision@5:  {p_at_5:.4f}")  # => shows precision@5
    print(f"precision@10: {p_at_10:.4f}")  # => shows precision@10

    hand_top5_hits: int = sum(
        1 for d in ranked[:5] if d in relevant
    )  # => hand count: {1,3,5} in the top 5
    hand_top10_hits: int = sum(
        1 for d in ranked[:10] if d in relevant
    )  # => hand count: {1,3,5,7,9} in the top 10
    assert p_at_5 == hand_top5_hits / 5, (
        "precision@5 must match a hand count of relevant docs in the first 5"
    )  # => precision@5 must match a hand count of relevant docs in the first 5
    assert p_at_10 == hand_top10_hits / 10, (
        "precision@10 must match a hand count of relevant docs in the first 10"
    )  # => precision@10 must match a hand count of relevant docs in the first 10
    print(
        f"MATCH: precision@5 ({p_at_5}) and precision@10 ({p_at_10}) both equal their hand-counted values"
    )  # => shows MATCH: precision@5 (


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end

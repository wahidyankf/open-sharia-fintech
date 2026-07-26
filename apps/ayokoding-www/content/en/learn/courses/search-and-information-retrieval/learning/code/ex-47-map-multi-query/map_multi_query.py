# pyright: strict
"""Example 47: MAP: Multi-Query (co-24)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def average_precision(
    ranked: list[int], relevant: set[int]
) -> float:  # => defines average precision
    if not relevant:  # => true when not relevant
        return 0.0  # => returns 0.0
    precisions_at_hits: list[float] = []  # => starts empty, populated by the loop below
    hits_so_far: int = 0  # => a running counter, starting at zero
    for k, doc_id in enumerate(ranked, start=1):  # => iterates one item at a time
        if doc_id in relevant:  # => true when doc_id in relevant
            hits_so_far += 1  # => advances hits_so_far
            precisions_at_hits.append(hits_so_far / k)  # => records this item, in order
    return sum(precisions_at_hits) / len(
        relevant
    )  # => returns sum(precisions_at_hits) / len(relevant)


def mean_average_precision(
    rankings: dict[str, list[int]], qrels: dict[str, set[int]]
) -> float:  # => mAP: the mean of average_precision across every query in the set
    """MAP: the mean of average_precision across every query in the set."""
    aps: list[float] = [
        average_precision(rankings[q], qrels[q]) for q in rankings
    ]  # => co-24: one AP per query
    return (
        sum(aps) / len(aps) if aps else 0.0
    )  # => returns sum(aps) / len(aps) if aps else 0.0


def main() -> None:  # => defines main
    rankings: dict[
        str, list[int]
    ] = {  # => 3 queries, each with its own ranked result list
        "q1": [1, 2, 3, 4],  # => entry for 'q1'
        "q2": [5, 6, 7, 8],  # => entry for 'q2'
        "q3": [9, 10, 11, 12],  # => entry for 'q3'
    }  # => opens/closes this multi-line literal
    qrels: dict[str, set[int]] = {  # => 3 queries, each with its own relevant-doc set
        "q1": {
            1,
            3,
        },  # => AP for q1: hits at rank 1 (p=1.0) and rank 3 (p=2/3) -> (1.0+0.6667)/2
        "q2": {
            5,
            6,
            7,
            8,
        },  # => AP for q2: every result is relevant, all hits at consecutive ranks -> AP = 1.0
        "q3": {12},  # => AP for q3: the only relevant doc is LAST -> AP = 1/4
    }  # => opens/closes this multi-line literal
    map_score: float = mean_average_precision(
        rankings, qrels
    )  # => co-24: one number over all 3 queries
    per_query_ap: dict[str, float] = {
        q: average_precision(rankings[q], qrels[q]) for q in rankings
    }  # => the per-query breakdown
    for q, ap in per_query_ap.items():  # => iterates one item at a time
        print(f"{q}: AP={ap:.4f}")  # => prints this step's result
    print(f"MAP: {map_score:.4f}")  # => shows MAP

    hand_ap_q1: float = (1 / 1 + 2 / 3) / 2  # => hits at rank 1 and rank 3
    hand_ap_q2: float = 1.0  # => every result relevant, in order -- perfect AP
    hand_ap_q3: float = (1 / 4) / 1  # => the only relevant doc is the LAST of 4 results
    hand_map: float = (
        hand_ap_q1 + hand_ap_q2 + hand_ap_q3
    ) / 3  # => hand map = (hand_ap_q1 + hand_ap_q2 + hand_ap_q3) / 3
    assert abs(map_score - hand_map) < 1e-9, (
        f"MAP must equal the hand-computed mean {hand_map}"
    )  # => MAP must equal the hand-computed mean {hand_map}
    print(
        f"MATCH: MAP={map_score:.4f} equals the hand-computed mean of the 3 per-query APs ({hand_map:.4f})"
    )  # => shows MATCH: MAP=


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end

# pyright: strict
"""Example 38: Top-K Heap (co-20)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import heapq  # => stdlib binary heap -- backs the size-k top-k selection
import random  # => stdlib PRNG -- reproducible synthetic fixtures and trials


def topk_via_heap(
    scored: list[tuple[float, int]], k: int
) -> list[
    tuple[float, int]
]:  # => return the k highest-scoring (score, doc_id) pairs using a size-k min-heap
    """Return the k highest-scoring (score, doc_id) pairs using a size-k min-heap."""
    heap: list[
        tuple[float, int]
    ] = []  # => co-20: a MIN-heap -- the smallest of the k kept sits at heap[0]
    for score, doc_id in scored:  # => iterates one item at a time
        if len(heap) < k:  # => true when len(heap) < k
            heapq.heappush(
                heap, (score, doc_id)
            )  # => co-20: heap not full yet -- always keep this candidate
        elif (
            score > heap[0][0]
        ):  # => co-20: only replace the WORST kept item if this candidate beats it
            heapq.heapreplace(
                heap, (score, doc_id)
            )  # => pop the min, push the new one, in one O(log k) step
    return sorted(
        heap, key=lambda sd: (-sd[0], sd[1])
    )  # => co-20: final k results, best score first


def topk_via_full_sort(
    scored: list[tuple[float, int]], k: int
) -> list[
    tuple[float, int]
]:  # => reference implementation: sort everything, take the first k
    """Reference implementation: sort everything, take the first k."""
    return sorted(scored, key=lambda sd: (-sd[0], sd[1]))[
        :k
    ]  # => returns sorted(scored, key=lambda sd: (-sd[0], sd[1]))[:k]


def main() -> None:  # => defines main
    rng = random.Random(7)  # => fixed seed -- reproducible
    scored: list[tuple[float, int]] = [
        (rng.uniform(0, 100), doc_id) for doc_id in range(1000)
    ]  # => 1000 (score, doc_id) pairs

    heap_result: list[tuple[float, int]] = topk_via_heap(
        scored, k=5
    )  # => co-20: the size-5 heap's own top-5
    sort_result: list[tuple[float, int]] = topk_via_full_sort(
        scored, k=5
    )  # => the reference: full sort, then slice
    print(
        f"heap top-5:  {[(round(s, 2), d) for s, d in heap_result]}"
    )  # => shows heap top-5
    print(
        f"sort top-5:  {[(round(s, 2), d) for s, d in sort_result]}"
    )  # => shows sort top-5

    assert heap_result == sort_result, (
        "the heap's top-5 must be IDENTICAL to the full sort's top-5"
    )  # => the heap's top-5 must be IDENTICAL to the full sort's top-5
    print(
        "MATCH: the size-5 min-heap returns exactly the same top-5 as a full sort over all 1000 scores"
    )  # => shows MATCH: the size-5 min-heap returns exactly the same top-5 as a full sort over all 1000 scores


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end

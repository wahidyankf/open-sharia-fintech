# pyright: strict
"""Example 39: Top-K vs Full Sort Timing (co-20)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import heapq  # => stdlib binary heap -- backs the size-k top-k selection
import random  # => stdlib PRNG -- reproducible synthetic fixtures and trials
import time  # => stdlib timer -- wall-clock measurement, not a benchmark micro-op
from typing import Callable  # => from typing: Callable


def topk_via_heap(
    scored: list[tuple[float, int]], k: int
) -> list[tuple[float, int]]:  # => defines topk via heap
    return heapq.nlargest(
        k, scored, key=lambda sd: sd[0]
    )  # => co-20: heapq's own optimized top-k


def topk_via_full_sort(
    scored: list[tuple[float, int]], k: int
) -> list[tuple[float, int]]:  # => defines topk via full sort
    return sorted(scored, key=lambda sd: -sd[0])[
        :k
    ]  # => returns sorted(scored, key=lambda sd: -sd[0])[:k]


def main() -> None:  # => defines main
    rng = random.Random(11)  # => fixed seed -- reproducible
    n: int = 500_000  # => a large scored corpus
    k: int = 10  # => a SMALL k relative to n -- exactly where a heap should win
    scored: list[tuple[float, int]] = [
        (rng.uniform(0, 100), doc_id) for doc_id in range(n)
    ]  # => scored = [(rng.uniform(0, 100), doc_id) for doc_id in ra...

    heap_result: list[tuple[float, int]] = topk_via_heap(
        scored, k
    )  # => correctness check first
    sort_result: list[tuple[float, int]] = topk_via_full_sort(
        scored, k
    )  # => sort result = topk_via_full_sort(scored, k)
    assert heap_result == sort_result, (
        "heap and full-sort top-k must be IDENTICAL before comparing speed"
    )  # => heap and full-sort top-k must be IDENTICAL before comparing speed

    heap_time: float = min(
        _time_call(lambda: topk_via_heap(scored, k)) for _ in range(3)
    )  # => best of 3 runs
    sort_time: float = min(
        _time_call(lambda: topk_via_full_sort(scored, k)) for _ in range(3)
    )  # => best of 3 runs
    print(
        f"n={n}, k={k}: heap={heap_time * 1000:.2f}ms  full_sort={sort_time * 1000:.2f}ms  ratio={sort_time / heap_time:.1f}x"
    )  # => shows n=

    assert heap_time < sort_time, (
        "the heap-based top-k must be FASTER than a full sort at this n and k"
    )  # => the heap-based top-k must be FASTER than a full sort at this n and k
    print(
        f"MATCH: identical top-{k} results, and the heap is {sort_time / heap_time:.1f}x faster than a full sort"
    )  # => shows MATCH: identical top


def _time_call(fn: Callable[[], object]) -> float:  # => defines  time call
    start: float = time.perf_counter()  # => start = time.perf_counter()
    fn()  # => part of this step's computation, continued from the line above
    return time.perf_counter() - start  # => returns time.perf_counter() - start


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end

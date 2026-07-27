"""Kata 3 (after): insert uses bisect.insort, so the leaf stays sorted by key after every insert."""

from __future__ import annotations

import bisect


def insert(leaf: list[tuple[int, int]], key: int, page_id: int) -> None:
    bisect.insort(
        leaf, (key, page_id)
    )  # => keeps `leaf` sorted by key on every single insert


def range_scan(
    leaf: list[tuple[int, int]], low: int, high: int
) -> list[tuple[int, int]]:
    return [(k, p) for k, p in leaf if low <= k <= high]


leaf: list[tuple[int, int]] = []
for key in [5, 1, 9, 3, 7]:
    insert(leaf, key, page_id=key * 10)
print(range_scan(leaf, 1, 7))
print(range_scan(leaf, 1, 7) == sorted(range_scan(leaf, 1, 7)))

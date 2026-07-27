"""Kata 3 (before): a B-tree leaf insert appends instead of sorting, breaking range_scan's ordering."""

from __future__ import annotations


def insert(leaf: list[tuple[int, int]], key: int, page_id: int) -> None:
    leaf.append(
        (key, page_id)
    )  # BUG: always appends -- the leaf is never actually kept SORTED by key


def range_scan(
    leaf: list[tuple[int, int]], low: int, high: int
) -> list[tuple[int, int]]:
    return [
        (k, p) for k, p in leaf if low <= k <= high
    ]  # relies on `leaf` already being sorted


leaf: list[tuple[int, int]] = []
for key in [5, 1, 9, 3, 7]:  # inserted out of order
    insert(leaf, key, page_id=key * 10)
print(range_scan(leaf, 1, 7))
print(
    range_scan(leaf, 1, 7) == sorted(range_scan(leaf, 1, 7))
)  # expected True -- a range scan MUST be sorted

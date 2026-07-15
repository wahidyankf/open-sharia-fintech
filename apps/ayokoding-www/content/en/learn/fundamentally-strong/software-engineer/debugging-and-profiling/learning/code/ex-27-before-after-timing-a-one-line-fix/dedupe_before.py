"""Example 27 (before): a quadratic dedupe -- one line makes this O(n^2)."""

from __future__ import annotations


def dedupe(values: list[int]) -> list[int]:
    result: list[int] = []
    for v in values:
        if v not in result:  # O(n) membership check on a list -- O(n^2) overall
            result.append(v)
    return result

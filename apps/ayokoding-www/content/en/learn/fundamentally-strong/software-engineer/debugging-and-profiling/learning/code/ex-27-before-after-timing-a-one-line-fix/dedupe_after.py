"""Example 27 (after): the one-line fix -- track membership with a set instead of a list."""

from __future__ import annotations


def dedupe(values: list[int]) -> list[int]:
    result: list[int] = []
    seen: set[int] = set()  # O(1) average membership check -- the one-line-family fix
    for v in values:
        if v not in seen:
            seen.add(v)
            result.append(v)
    return result

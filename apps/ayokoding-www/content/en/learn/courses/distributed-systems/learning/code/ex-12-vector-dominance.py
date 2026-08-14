"""Runnable artifact for distributed-systems Example 12."""

from __future__ import annotations

before: dict[str, int] = {"a": 1, "b": 0}
after: dict[str, int] = {"a": 2, "b": 1}
dominates: bool = (
    all(before[node] <= after[node] for node in before) and before != after
)
# => Strict vector dominance represents happened-before.
assert dominates
print(dominates)

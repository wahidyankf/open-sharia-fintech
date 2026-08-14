"""Runnable artifact for distributed-systems Example 69."""

from __future__ import annotations

left: dict[str, int] = {"a": 2, "b": 0}
right: dict[str, int] = {"a": 1, "b": 3}
merged: dict[str, int] = {node: max(left[node], right[node]) for node in left}
# => Component maxima retain concurrent grow-only increments.
assert sum(merged.values()) == 5
print(merged)

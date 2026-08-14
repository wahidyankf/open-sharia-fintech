"""Runnable artifact for distributed-systems Example 36."""

from __future__ import annotations

left: dict[str, int] = {"a": 2, "b": 0}
right: dict[str, int] = {"a": 1, "b": 1}
comparable: bool = all(left[k] <= right[k] for k in left) or all(
    right[k] <= left[k] for k in left
)
# => Incomparable vectors preserve a conflict for policy to resolve.
assert not comparable
print("conflict")

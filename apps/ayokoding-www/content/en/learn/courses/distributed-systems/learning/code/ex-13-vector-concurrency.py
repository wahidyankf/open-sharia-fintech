"""Runnable artifact for distributed-systems Example 13."""

from __future__ import annotations

left: dict[str, int] = {"a": 2, "b": 0}
right: dict[str, int] = {"a": 1, "b": 1}
left_before_right: bool = all(left[node] <= right[node] for node in left)
right_before_left: bool = all(right[node] <= left[node] for node in left)
# => Neither vector dominates, so the events are concurrent.
assert not left_before_right and not right_before_left
print("concurrent")

# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 13."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
left: dict[str, int] = {"a": 2, "b": 0}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
right: dict[str, int] = {"a": 1, "b": 1}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
left_before_right: bool = all(left[node] <= right[node] for node in left)
# => This keeps the modeled rule explicit so its trade-off can be inspected.
right_before_left: bool = all(right[node] <= left[node] for node in left)
# => Neither vector dominates, so the events are concurrent.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert not left_before_right and not right_before_left
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print("concurrent")

# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 69."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
left: dict[str, int] = {"a": 2, "b": 0}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
right: dict[str, int] = {"a": 1, "b": 3}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
merged: dict[str, int] = {node: max(left[node], right[node]) for node in left}
# => Component maxima retain concurrent grow-only increments.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert sum(merged.values()) == 5
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(merged)

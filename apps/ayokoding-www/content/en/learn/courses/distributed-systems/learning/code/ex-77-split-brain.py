# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 77."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
leaders: dict[str, str] = {"partition-a": "node-1", "partition-b": "node-2"}
# => Separate partitions naming different leaders demonstrate split brain.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert len(set(leaders.values())) == 2
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(leaders)

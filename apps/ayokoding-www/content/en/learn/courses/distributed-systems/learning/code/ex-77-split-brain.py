"""Runnable artifact for distributed-systems Example 77."""

from __future__ import annotations

leaders: dict[str, str] = {"partition-a": "node-1", "partition-b": "node-2"}
# => Separate partitions naming different leaders demonstrate split brain.
assert len(set(leaders.values())) == 2
print(leaders)

"""Runnable artifact for distributed-systems Example 63."""

from __future__ import annotations

partition_size: int = 2
total_members: int = 3
can_elect: bool = partition_size > total_members // 2
# => Only the majority side can elect a legitimate leader.
assert can_elect
print(can_elect)

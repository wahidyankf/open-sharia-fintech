# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 63."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
partition_size: int = 2
# => This keeps the modeled rule explicit so its trade-off can be inspected.
total_members: int = 3
# => This keeps the modeled rule explicit so its trade-off can be inspected.
can_elect: bool = partition_size > total_members // 2
# => Only the majority side can elect a legitimate leader.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert can_elect
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(can_elect)

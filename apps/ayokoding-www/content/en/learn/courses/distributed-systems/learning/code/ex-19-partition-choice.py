# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 19."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
partitioned: bool = True
# => This keeps the modeled rule explicit so its trade-off can be inspected.
choice: str = "consistency"
# => This keeps the modeled rule explicit so its trade-off can be inspected.
result: str = "reject" if partitioned and choice == "consistency" else "accept"
# => A CP operation exposes unavailability during a partition.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert result == "reject"
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(result)

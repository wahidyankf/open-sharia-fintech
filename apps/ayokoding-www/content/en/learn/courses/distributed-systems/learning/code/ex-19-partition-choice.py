"""Runnable artifact for distributed-systems Example 19."""

from __future__ import annotations

partitioned: bool = True
choice: str = "consistency"
result: str = "reject" if partitioned and choice == "consistency" else "accept"
# => A CP operation exposes unavailability during a partition.
assert result == "reject"
print(result)

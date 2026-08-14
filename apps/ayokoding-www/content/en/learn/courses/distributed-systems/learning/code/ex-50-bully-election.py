"""Runnable artifact for distributed-systems Example 50."""

from __future__ import annotations

live: list[int] = [1, 3, 2]
leader: int = max(live)
# => The highest responding identifier wins this simplified election.
assert leader == 3
print(leader)

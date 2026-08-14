# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 50."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
live: list[int] = [1, 3, 2]
# => This keeps the modeled rule explicit so its trade-off can be inspected.
leader: int = max(live)
# => The highest responding identifier wins this simplified election.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert leader == 3
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(leader)

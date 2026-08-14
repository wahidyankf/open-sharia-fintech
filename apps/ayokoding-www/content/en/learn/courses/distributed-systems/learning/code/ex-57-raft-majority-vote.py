# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 57."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
votes: int = 2
# => This keeps the modeled rule explicit so its trade-off can be inspected.
members: int = 3
# => This keeps the modeled rule explicit so its trade-off can be inspected.
won: bool = votes > members // 2
# => A minority cannot claim Raft leadership.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert won
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(won)

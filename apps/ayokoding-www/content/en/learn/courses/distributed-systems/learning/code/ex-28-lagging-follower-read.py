# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 28."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
leader: str = "paid"
# => This keeps the modeled rule explicit so its trade-off can be inspected.
follower: str = "pending"
# => A follower can answer before it applies the leader's newest value.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert follower != leader
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(follower)

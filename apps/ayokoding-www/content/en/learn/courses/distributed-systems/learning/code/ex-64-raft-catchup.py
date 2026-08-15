# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 64."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
leader: list[str] = ["a", "b", "c"]
# => This keeps the modeled rule explicit so its trade-off can be inspected.
follower: list[str] = ["a"]
# => This keeps the modeled rule explicit so its trade-off can be inspected.
follower[:] = leader
# => Healing requires explicit catch-up to the committed leader prefix.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert follower == leader
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(follower)

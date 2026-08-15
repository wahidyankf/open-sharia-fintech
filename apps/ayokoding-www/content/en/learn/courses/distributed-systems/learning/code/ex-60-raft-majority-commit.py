# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 60."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
replicated_on: int = 2
# => This keeps the modeled rule explicit so its trade-off can be inspected.
members: int = 3
# => This keeps the modeled rule explicit so its trade-off can be inspected.
committed: bool = replicated_on > members // 2
# => Quorum storage, not leader-local append, advances commitment.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert committed
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(committed)

"""Runnable artifact for distributed-systems Example 60."""

from __future__ import annotations

replicated_on: int = 2
members: int = 3
committed: bool = replicated_on > members // 2
# => Quorum storage, not leader-local append, advances commitment.
assert committed
print(committed)

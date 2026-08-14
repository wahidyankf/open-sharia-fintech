"""Runnable artifact for distributed-systems Example 57."""

from __future__ import annotations

votes: int = 2
members: int = 3
won: bool = votes > members // 2
# => A minority cannot claim Raft leadership.
assert won
print(won)

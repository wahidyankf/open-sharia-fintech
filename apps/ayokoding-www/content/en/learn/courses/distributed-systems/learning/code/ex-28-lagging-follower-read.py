"""Runnable artifact for distributed-systems Example 28."""

from __future__ import annotations

leader: str = "paid"
follower: str = "pending"
# => A follower can answer before it applies the leader's newest value.
assert follower != leader
print(follower)

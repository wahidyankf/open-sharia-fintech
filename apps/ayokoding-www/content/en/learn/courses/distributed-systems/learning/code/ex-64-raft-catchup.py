"""Runnable artifact for distributed-systems Example 64."""

from __future__ import annotations

leader: list[str] = ["a", "b", "c"]
follower: list[str] = ["a"]
follower[:] = leader
# => Healing requires explicit catch-up to the committed leader prefix.
assert follower == leader
print(follower)

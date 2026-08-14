"""Runnable artifact for distributed-systems Example 51."""

from __future__ import annotations

ring: list[int] = [2, 1, 3]
token: list[int] = []
token.extend(ring)
# => One completed ring pass includes every reachable candidate.
assert max(token) == 3
print(token)

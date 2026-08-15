# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 51."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
ring: list[int] = [2, 1, 3]
# => This keeps the modeled rule explicit so its trade-off can be inspected.
token: list[int] = []
# => This keeps the modeled rule explicit so its trade-off can be inspected.
token.extend(ring)
# => One completed ring pass includes every reachable candidate.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert max(token) == 3
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(token)

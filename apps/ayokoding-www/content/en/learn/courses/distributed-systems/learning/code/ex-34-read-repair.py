"""Runnable artifact for distributed-systems Example 34."""

from __future__ import annotations

fresh: dict[str, int] = {"v": 2}
stale: dict[str, int] = {"v": 1}
stale.update(fresh)
# => Seeing a newer version repairs a lagging replica.
assert stale["v"] == 2
print(stale)

# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 34."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
fresh: dict[str, int] = {"v": 2}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
stale: dict[str, int] = {"v": 1}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
stale.update(fresh)
# => Seeing a newer version repairs a lagging replica.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert stale["v"] == 2
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(stale)

# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 74."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
faults: int = 1
# => This keeps the modeled rule explicit so its trade-off can be inspected.
members: int = 4
# => PBFT requires at least 3f + 1 replicas for f Byzantine faults.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert members >= 3 * faults + 1
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(members)

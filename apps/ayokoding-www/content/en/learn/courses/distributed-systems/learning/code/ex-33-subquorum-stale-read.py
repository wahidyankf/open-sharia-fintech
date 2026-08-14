# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 33."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
members: int = 3
# => This keeps the modeled rule explicit so its trade-off can be inspected.
read_quorum: int = 1
# => This keeps the modeled rule explicit so its trade-off can be inspected.
write_quorum: int = 1
# => Disjoint one-replica choices permit a stale read.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert read_quorum + write_quorum <= members
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print("staleness permitted")

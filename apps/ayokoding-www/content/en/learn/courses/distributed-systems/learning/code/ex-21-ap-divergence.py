# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 21."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
replica_a: str = "A"
# => This keeps the modeled rule explicit so its trade-off can be inspected.
replica_b: str = "B"
# => Independent partition-side writes may diverge temporarily.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert replica_a != replica_b
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print((replica_a, replica_b))

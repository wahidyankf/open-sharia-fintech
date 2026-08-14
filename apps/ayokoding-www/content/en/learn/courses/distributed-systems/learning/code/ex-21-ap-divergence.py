"""Runnable artifact for distributed-systems Example 21."""

from __future__ import annotations

replica_a: str = "A"
replica_b: str = "B"
# => Independent partition-side writes may diverge temporarily.
assert replica_a != replica_b
print((replica_a, replica_b))

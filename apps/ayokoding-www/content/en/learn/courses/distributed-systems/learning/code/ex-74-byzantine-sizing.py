"""Runnable artifact for distributed-systems Example 74."""

from __future__ import annotations

faults: int = 1
members: int = 4
# => PBFT requires at least 3f + 1 replicas for f Byzantine faults.
assert members >= 3 * faults + 1
print(members)

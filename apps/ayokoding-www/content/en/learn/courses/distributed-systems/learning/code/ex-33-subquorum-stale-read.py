"""Runnable artifact for distributed-systems Example 33."""

from __future__ import annotations

members: int = 3
read_quorum: int = 1
write_quorum: int = 1
# => Disjoint one-replica choices permit a stale read.
assert read_quorum + write_quorum <= members
print("staleness permitted")

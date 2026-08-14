"""Runnable artifact for distributed-systems Example 22."""

from __future__ import annotations

near_replica_value: str = "stale"
leader_value: str = "fresh"
fast_read: str = near_replica_value
# => Choosing local latency can intentionally return a stale normal-path read.
assert fast_read == "stale" and fast_read != leader_value
print(fast_read)

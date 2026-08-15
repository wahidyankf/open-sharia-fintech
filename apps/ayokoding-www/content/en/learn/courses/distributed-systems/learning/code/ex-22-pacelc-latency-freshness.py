# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 22."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
near_replica_value: str = "stale"
# => This keeps the modeled rule explicit so its trade-off can be inspected.
leader_value: str = "fresh"
# => This keeps the modeled rule explicit so its trade-off can be inspected.
fast_read: str = near_replica_value
# => Choosing local latency can intentionally return a stale normal-path read.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert fast_read == "stale" and fast_read != leader_value
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(fast_read)

# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 58."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
role: str = "follower"
# => This keeps the modeled rule explicit so its trade-off can be inspected.
received_heartbeat: bool = True
# => This keeps the modeled rule explicit so its trade-off can be inspected.
start_election: bool = role == "follower" and not received_heartbeat
# => A valid leader heartbeat suppresses unnecessary elections.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert not start_election
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(start_election)

"""Runnable artifact for distributed-systems Example 58."""

from __future__ import annotations

role: str = "follower"
received_heartbeat: bool = True
start_election: bool = role == "follower" and not received_heartbeat
# => A valid leader heartbeat suppresses unnecessary elections.
assert not start_election
print(start_election)

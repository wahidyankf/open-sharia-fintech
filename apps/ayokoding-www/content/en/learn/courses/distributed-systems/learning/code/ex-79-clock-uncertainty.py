"""Runnable artifact for distributed-systems Example 79."""

from __future__ import annotations

# => The lower bound models the earliest possible current time in the uncertainty interval.
earliest: int = 100
# => The assigned commit timestamp must be known before the acknowledgement is safe.
assigned_commit: int = 103
# => Commit-wait advances the modeled lower bound until real time must have passed that timestamp.
while earliest <= assigned_commit:
    earliest += 1
# => Only a lower bound beyond the assigned timestamp establishes the required ordering fact.
safe_to_ack: bool = earliest > assigned_commit
# => This assertion proves the simulation waited rather than comparing only an upper bound.
assert safe_to_ack
# => The printed result represents the point at which this simplified model may acknowledge.
print(safe_to_ack)

"""Runnable artifact for distributed-systems Example 79."""

from __future__ import annotations

now: int = 100
uncertainty: int = 5
prior_commit: int = 103
safe_to_ack: bool = now + uncertainty > prior_commit
# => The uncertainty upper bound must pass the earlier commit before acknowledgement.
assert safe_to_ack
print(safe_to_ack)

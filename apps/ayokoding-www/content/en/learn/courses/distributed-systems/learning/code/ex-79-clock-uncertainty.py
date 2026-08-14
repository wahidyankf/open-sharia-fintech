# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 79."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
now: int = 100
# => This keeps the modeled rule explicit so its trade-off can be inspected.
uncertainty: int = 5
# => This keeps the modeled rule explicit so its trade-off can be inspected.
prior_commit: int = 103
# => This keeps the modeled rule explicit so its trade-off can be inspected.
safe_to_ack: bool = now + uncertainty > prior_commit
# => The uncertainty upper bound must pass the earlier commit before acknowledgement.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert safe_to_ack
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(safe_to_ack)

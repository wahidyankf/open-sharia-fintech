# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 30."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
acks: int = 1
# => This keeps the modeled rule explicit so its trade-off can be inspected.
required: int = 2
# => This keeps the modeled rule explicit so its trade-off can be inspected.
accepted: bool = acks >= required
# => A below-quorum write cannot report quorum success.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert not accepted
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(accepted)

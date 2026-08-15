# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 31."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
responses: list[str] = ["new"]
# => This keeps the modeled rule explicit so its trade-off can be inspected.
required: int = 2
# => This keeps the modeled rule explicit so its trade-off can be inspected.
accepted: bool = len(responses) >= required
# => One response cannot satisfy a two-replica read contract.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert not accepted
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(accepted)

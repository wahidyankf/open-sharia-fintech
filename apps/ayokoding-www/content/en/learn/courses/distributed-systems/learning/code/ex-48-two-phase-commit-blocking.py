# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 48."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
prepared: bool = True
# => This keeps the modeled rule explicit so its trade-off can be inspected.
coordinator_alive: bool = False
# => This keeps the modeled rule explicit so its trade-off can be inspected.
state: str = "blocked" if prepared and not coordinator_alive else "finished"
# => A prepared participant cannot safely invent the missing decision.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert state == "blocked"
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(state)

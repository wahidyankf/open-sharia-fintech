"""Runnable artifact for distributed-systems Example 48."""

from __future__ import annotations

prepared: bool = True
coordinator_alive: bool = False
state: str = "blocked" if prepared and not coordinator_alive else "finished"
# => A prepared participant cannot safely invent the missing decision.
assert state == "blocked"
print(state)

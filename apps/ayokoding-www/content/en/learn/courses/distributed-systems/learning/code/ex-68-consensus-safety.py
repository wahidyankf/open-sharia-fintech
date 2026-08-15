# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 68."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
chosen_values: set[str] = {"approve"}
# => Consensus safety forbids two chosen values for one decision.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert len(chosen_values) == 1
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(chosen_values)

# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 85."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from dataclasses import dataclass


# => This keeps the modeled rule explicit so its trade-off can be inspected.
@dataclass(frozen=True)
# => This keeps the modeled rule explicit so its trade-off can be inspected.
class Choice:
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    benefit: str
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    cost: str


# => This keeps the modeled rule explicit so its trade-off can be inspected.
options: dict[str, Choice] = {
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    "coordination-service": Choice("mature leases and watches", "operate a dependency"),
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    "hand-rolled-consensus": Choice("learning control", "high correctness cost"),
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
}
# => Select a mature service unless implementing consensus is the explicit learning goal.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
selected: str = "coordination-service"
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert selected in options and "leases" in options[selected].benefit
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(selected)

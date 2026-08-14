"""Runnable artifact for distributed-systems Example 85."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Choice:
    benefit: str
    cost: str


options: dict[str, Choice] = {
    "coordination-service": Choice("mature leases and watches", "operate a dependency"),
    "hand-rolled-consensus": Choice("learning control", "high correctness cost"),
}
# => Select a mature service unless implementing consensus is the explicit learning goal.
selected: str = "coordination-service"
assert selected in options and "leases" in options[selected].benefit
print(selected)

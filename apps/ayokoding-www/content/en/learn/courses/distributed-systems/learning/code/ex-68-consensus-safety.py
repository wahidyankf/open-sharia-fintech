"""Runnable artifact for distributed-systems Example 68."""

from __future__ import annotations

chosen_values: set[str] = {"approve"}
# => Consensus safety forbids two chosen values for one decision.
assert len(chosen_values) == 1
print(chosen_values)

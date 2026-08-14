"""Runnable artifact for distributed-systems Example 37."""

from __future__ import annotations

missed: int = 3
threshold: int = 3
suspect: bool = missed >= threshold
# => Silence reaches a policy threshold, not physical proof of failure.
assert suspect
print(suspect)

"""Runnable artifact for distributed-systems Example 52."""

from __future__ import annotations

left: set[str] = {"a", "b"}
right: set[str] = {"b", "c"}
merged: set[str] = left | right
# => A commutative merge lets replicas exchange missing observations.
assert merged == {"a", "b", "c"}
print(sorted(merged))

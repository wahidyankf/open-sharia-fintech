"""Runnable artifact for distributed-systems Example 71."""

from __future__ import annotations

left: set[str] = {"a", "b"}
right: set[str] = {"b", "c"}
merged: set[str] = left | right
# => Union is associative, commutative, and idempotent.
assert merged == {"a", "b", "c"}
print(sorted(merged))

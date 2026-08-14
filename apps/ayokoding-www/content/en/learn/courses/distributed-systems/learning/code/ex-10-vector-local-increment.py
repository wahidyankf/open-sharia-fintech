"""Runnable artifact for distributed-systems Example 10."""

from __future__ import annotations

clock: dict[str, int] = {"a": 0, "b": 0}
clock["a"] += 1
# => A node increments only its own vector coordinate.
assert clock == {"a": 1, "b": 0}
print(clock)

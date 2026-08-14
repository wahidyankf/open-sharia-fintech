"""Runnable artifact for distributed-systems Example 5."""

from __future__ import annotations

clock: int = 0
clock += 1
# => Every local event advances logical time monotonically.
assert clock == 1
print(clock)

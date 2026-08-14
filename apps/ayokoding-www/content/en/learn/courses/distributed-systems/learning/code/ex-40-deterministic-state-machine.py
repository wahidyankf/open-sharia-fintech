"""Runnable artifact for distributed-systems Example 40."""

from __future__ import annotations

log: list[int] = [1, 2, 3]
state_a: int = 0
state_b: int = 0
for command in log:
    state_a += command
    state_b += command
# => Same commands in the same order give identical state.
assert state_a == state_b == 6
print(state_a)

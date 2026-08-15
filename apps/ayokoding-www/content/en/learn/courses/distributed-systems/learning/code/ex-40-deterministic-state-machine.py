# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 40."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
log: list[int] = [1, 2, 3]
# => This keeps the modeled rule explicit so its trade-off can be inspected.
state_a: int = 0
# => This keeps the modeled rule explicit so its trade-off can be inspected.
state_b: int = 0
# => This keeps the modeled rule explicit so its trade-off can be inspected.
for command in log:
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    state_a += command
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    state_b += command
# => Same commands in the same order give identical state.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert state_a == state_b == 6
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(state_a)

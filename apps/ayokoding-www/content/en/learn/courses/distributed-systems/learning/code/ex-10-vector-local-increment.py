# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 10."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
clock: dict[str, int] = {"a": 0, "b": 0}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
clock["a"] += 1
# => A node increments only its own vector coordinate.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert clock == {"a": 1, "b": 0}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(clock)

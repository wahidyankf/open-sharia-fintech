# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 5."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
clock: int = 0
# => This keeps the modeled rule explicit so its trade-off can be inspected.
clock += 1
# => Every local event advances logical time monotonically.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert clock == 1
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(clock)

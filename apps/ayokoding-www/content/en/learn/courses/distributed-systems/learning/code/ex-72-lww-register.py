# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 72."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
left: tuple[int, str] = (10, "blue")
# => This keeps the modeled rule explicit so its trade-off can be inspected.
right: tuple[int, str] = (12, "teal")
# => This keeps the modeled rule explicit so its trade-off can be inspected.
winner: tuple[int, str] = max(left, right)
# => The greater supplied timestamp determines the visible register value.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert winner == right
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(winner)

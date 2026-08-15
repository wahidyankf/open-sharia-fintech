# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 35."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
left: tuple[int, str] = (5, "left")
# => This keeps the modeled rule explicit so its trade-off can be inspected.
right: tuple[int, str] = (7, "right")
# => This keeps the modeled rule explicit so its trade-off can be inspected.
winner: tuple[int, str] = max(left, right)
# => The larger ordering key wins even when writes were concurrent.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert winner == right
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(winner)

"""Runnable artifact for distributed-systems Example 35."""

from __future__ import annotations

left: tuple[int, str] = (5, "left")
right: tuple[int, str] = (7, "right")
winner: tuple[int, str] = max(left, right)
# => The larger ordering key wins even when writes were concurrent.
assert winner == right
print(winner)

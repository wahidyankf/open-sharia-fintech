"""Runnable artifact for distributed-systems Example 72."""

from __future__ import annotations

left: tuple[int, str] = (10, "blue")
right: tuple[int, str] = (12, "teal")
winner: tuple[int, str] = max(left, right)
# => The greater supplied timestamp determines the visible register value.
assert winner == right
print(winner)

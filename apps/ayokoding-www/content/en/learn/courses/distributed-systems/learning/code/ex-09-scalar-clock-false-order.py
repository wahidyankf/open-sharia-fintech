# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 9."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
event_a: tuple[int, str] = (4, "node-a")
# => This keeps the modeled rule explicit so its trade-off can be inspected.
event_b: tuple[int, str] = (4, "node-b")
# => This keeps the modeled rule explicit so its trade-off can be inspected.
ordered: list[tuple[int, str]] = sorted([event_a, event_b])
# => Sorting concurrent scalar timestamps is a tie-break, not evidence.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert ordered[0] == event_a
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(ordered)

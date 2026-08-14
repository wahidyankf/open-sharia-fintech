"""Runnable artifact for distributed-systems Example 9."""

from __future__ import annotations

event_a: tuple[int, str] = (4, "node-a")
event_b: tuple[int, str] = (4, "node-b")
ordered: list[tuple[int, str]] = sorted([event_a, event_b])
# => Sorting concurrent scalar timestamps is a tie-break, not evidence.
assert ordered[0] == event_a
print(ordered)

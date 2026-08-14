"""Runnable artifact for distributed-systems Example 7."""

from __future__ import annotations

events: list[tuple[int, str]] = [(5, "node-b"), (5, "node-a")]
ordered: list[tuple[int, str]] = sorted(events)
# => Process identity creates a deterministic order without proving causality.
assert ordered == [(5, "node-a"), (5, "node-b")]
print(ordered)

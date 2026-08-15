# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 7."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
events: list[tuple[int, str]] = [(5, "node-b"), (5, "node-a")]
# => This keeps the modeled rule explicit so its trade-off can be inspected.
ordered: list[tuple[int, str]] = sorted(events)
# => Process identity creates a deterministic order without proving causality.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert ordered == [(5, "node-a"), (5, "node-b")]
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(ordered)

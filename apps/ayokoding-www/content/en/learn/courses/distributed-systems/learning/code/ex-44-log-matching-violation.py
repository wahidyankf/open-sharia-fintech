# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 44."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
left: list[tuple[int, str]] = [(1, "a"), (2, "b")]
# => This keeps the modeled rule explicit so its trade-off can be inspected.
right: list[tuple[int, str]] = [(1, "a"), (2, "c")]
# => This keeps the modeled rule explicit so its trade-off can be inspected.
matching: bool = left == right
# => Different commands at one logical position cannot be one shared log.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert not matching
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(matching)

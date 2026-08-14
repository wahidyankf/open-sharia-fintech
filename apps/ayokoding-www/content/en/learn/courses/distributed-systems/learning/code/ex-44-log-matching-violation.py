"""Runnable artifact for distributed-systems Example 44."""

from __future__ import annotations

left: list[tuple[int, str]] = [(1, "a"), (2, "b")]
right: list[tuple[int, str]] = [(1, "a"), (2, "c")]
matching: bool = left == right
# => Different commands at one logical position cannot be one shared log.
assert not matching
print(matching)

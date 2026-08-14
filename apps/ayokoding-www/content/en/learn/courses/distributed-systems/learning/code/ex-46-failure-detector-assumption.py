"""Runnable artifact for distributed-systems Example 46."""

from __future__ import annotations

missed: int = 4
threshold: int = 3
replace_peer: bool = missed >= threshold
# => Progress comes from an explicit, fallible timeout assumption.
assert replace_peer
print(replace_peer)

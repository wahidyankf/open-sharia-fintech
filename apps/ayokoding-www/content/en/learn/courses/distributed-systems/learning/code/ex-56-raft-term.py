"""Runnable artifact for distributed-systems Example 56."""

from __future__ import annotations

old_term: int = 5
new_term: int = 6
# => Terms distinguish newer election authority from older authority.
assert new_term > old_term
print(new_term)

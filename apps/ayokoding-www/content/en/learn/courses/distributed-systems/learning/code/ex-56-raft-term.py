# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 56."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
old_term: int = 5
# => This keeps the modeled rule explicit so its trade-off can be inspected.
new_term: int = 6
# => Terms distinguish newer election authority from older authority.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert new_term > old_term
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(new_term)

# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 55."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
role: str = "follower"
# => This keeps the modeled rule explicit so its trade-off can be inspected.
term: int = 4
# => This keeps the modeled rule explicit so its trade-off can be inspected.
role, term = "candidate", term + 1
# => Election is an explicit transition into a new term.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert (role, term) == ("candidate", 5)
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print((role, term))

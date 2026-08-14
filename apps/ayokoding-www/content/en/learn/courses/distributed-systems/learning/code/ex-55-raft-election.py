"""Runnable artifact for distributed-systems Example 55."""

from __future__ import annotations

role: str = "follower"
term: int = 4
role, term = "candidate", term + 1
# => Election is an explicit transition into a new term.
assert (role, term) == ("candidate", 5)
print((role, term))

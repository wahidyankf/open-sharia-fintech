"""Runnable artifact for distributed-systems Example 62."""

from __future__ import annotations

role: str = "leader"
local_term: int = 4
observed_term: int = 5
if observed_term > local_term:
    role, local_term = "follower", observed_term
# => Higher-term evidence fences the older leader.
assert (role, local_term) == ("follower", 5)
print((role, local_term))

# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 62."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
role: str = "leader"
# => This keeps the modeled rule explicit so its trade-off can be inspected.
local_term: int = 4
# => This keeps the modeled rule explicit so its trade-off can be inspected.
observed_term: int = 5
# => This keeps the modeled rule explicit so its trade-off can be inspected.
if observed_term > local_term:
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    role, local_term = "follower", observed_term
# => Higher-term evidence fences the older leader.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert (role, local_term) == ("follower", 5)
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print((role, local_term))

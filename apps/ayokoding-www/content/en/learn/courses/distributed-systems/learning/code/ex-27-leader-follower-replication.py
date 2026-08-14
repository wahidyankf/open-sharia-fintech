# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 27."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
leader: list[str] = ["set:x=1"]
# => This keeps the modeled rule explicit so its trade-off can be inspected.
followers: list[list[str]] = [[], []]
# => This keeps the modeled rule explicit so its trade-off can be inspected.
for follower in followers:
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    follower.extend(leader)
# => Followers copy the leader's ordered entry.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert all(follower == leader for follower in followers)
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(followers)

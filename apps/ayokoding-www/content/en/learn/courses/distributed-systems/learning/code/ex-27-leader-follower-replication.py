"""Runnable artifact for distributed-systems Example 27."""

from __future__ import annotations

leader: list[str] = ["set:x=1"]
followers: list[list[str]] = [[], []]
for follower in followers:
    follower.extend(leader)
# => Followers copy the leader's ordered entry.
assert all(follower == leader for follower in followers)
print(followers)

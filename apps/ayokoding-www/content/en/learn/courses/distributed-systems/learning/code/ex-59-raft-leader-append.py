"""Runnable artifact for distributed-systems Example 59."""

from __future__ import annotations

leader_log: list[str] = ["set:x=1"]
follower_log: list[str] = []
follower_log.extend(leader_log)
# => A successful append gives the follower the leader's ordered entry.
assert follower_log == leader_log
print(follower_log)

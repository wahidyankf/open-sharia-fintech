# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 59."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
leader_log: list[str] = ["set:x=1"]
# => This keeps the modeled rule explicit so its trade-off can be inspected.
follower_log: list[str] = []
# => This keeps the modeled rule explicit so its trade-off can be inspected.
follower_log.extend(leader_log)
# => A successful append gives the follower the leader's ordered entry.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert follower_log == leader_log
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(follower_log)

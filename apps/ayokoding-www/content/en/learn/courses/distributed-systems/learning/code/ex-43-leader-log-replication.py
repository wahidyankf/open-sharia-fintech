# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 43."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
leader_log: list[str] = ["a", "b"]
# => This keeps the modeled rule explicit so its trade-off can be inspected.
follower_log: list[str] = ["a"]
# => This keeps the modeled rule explicit so its trade-off can be inspected.
follower_log.append(leader_log[1])
# => The follower extends its acknowledged matching prefix in order.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert follower_log == leader_log
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(follower_log)

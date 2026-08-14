"""Runnable artifact for distributed-systems Example 43."""

from __future__ import annotations

leader_log: list[str] = ["a", "b"]
follower_log: list[str] = ["a"]
follower_log.append(leader_log[1])
# => The follower extends its acknowledged matching prefix in order.
assert follower_log == leader_log
print(follower_log)

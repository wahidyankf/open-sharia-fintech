"""Runnable artifact for distributed-systems Example 45."""

from __future__ import annotations

message_arrived: bool = False
decision: str = "wait" if not message_arrived else "decide"
# => In a fully asynchronous model, silence need not become a decision.
assert decision == "wait"
print(decision)

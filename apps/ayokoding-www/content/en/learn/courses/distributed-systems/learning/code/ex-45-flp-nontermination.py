# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 45."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
message_arrived: bool = False
# => This keeps the modeled rule explicit so its trade-off can be inspected.
decision: str = "wait" if not message_arrived else "decide"
# => In a fully asynchronous model, silence need not become a decision.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert decision == "wait"
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(decision)

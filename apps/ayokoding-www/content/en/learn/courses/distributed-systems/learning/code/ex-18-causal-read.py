# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 18."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
history: list[str] = ["create order", "mark order paid"]
# => A dependent update remains after its observed cause.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert history.index("create order") < history.index("mark order paid")
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(history)

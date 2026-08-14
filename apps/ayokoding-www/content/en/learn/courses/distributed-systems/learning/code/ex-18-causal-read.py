"""Runnable artifact for distributed-systems Example 18."""

from __future__ import annotations

history: list[str] = ["create order", "mark order paid"]
# => A dependent update remains after its observed cause.
assert history.index("create order") < history.index("mark order paid")
print(history)

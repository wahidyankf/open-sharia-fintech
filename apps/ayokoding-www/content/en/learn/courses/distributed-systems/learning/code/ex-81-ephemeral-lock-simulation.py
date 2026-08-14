# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 81."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from dataclasses import dataclass


# => This keeps the modeled rule explicit so its trade-off can be inspected.
@dataclass(frozen=True)
# => This keeps the modeled rule explicit so its trade-off can be inspected.
class EphemeralNode:
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    path: str
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    session: str


# => This keeps the modeled rule explicit so its trade-off can be inspected.
nodes: list[EphemeralNode] = [EphemeralNode("/locks/order-0000000042", "holder")]
# => This keeps the modeled rule explicit so its trade-off can be inspected.
session_alive: bool = False
# => This keeps the modeled rule explicit so its trade-off can be inspected.
remaining: list[EphemeralNode] = [
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    node
    for node in nodes
    if session_alive or node.session != "holder"
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
]
# => Session loss removes its ephemeral claim without a client-side unlock.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert remaining == []
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(remaining)

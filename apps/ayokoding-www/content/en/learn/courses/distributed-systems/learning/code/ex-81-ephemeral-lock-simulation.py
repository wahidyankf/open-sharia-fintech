"""Runnable artifact for distributed-systems Example 81."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EphemeralNode:
    path: str
    session: str


nodes: list[EphemeralNode] = [EphemeralNode("/locks/order-0000000042", "holder")]
session_alive: bool = False
remaining: list[EphemeralNode] = [
    node for node in nodes if session_alive or node.session != "holder"
]
# => Session loss removes its ephemeral claim without a client-side unlock.
assert remaining == []
print(remaining)

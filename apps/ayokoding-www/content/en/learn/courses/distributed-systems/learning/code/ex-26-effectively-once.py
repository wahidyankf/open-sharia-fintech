"""Runnable artifact for distributed-systems Example 26."""

from __future__ import annotations

attempts: list[str] = ["m-1", "m-1"]
balance: int = 0
processed: set[str] = set()
for message_id in attempts:
    if message_id not in processed:
        processed.add(message_id)
        balance += 10
# => At-least-once transport plus idempotency yields one net effect.
assert balance == 10
print(balance)

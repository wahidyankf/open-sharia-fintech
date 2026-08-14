# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 26."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
attempts: list[str] = ["m-1", "m-1"]
# => This keeps the modeled rule explicit so its trade-off can be inspected.
balance: int = 0
# => This keeps the modeled rule explicit so its trade-off can be inspected.
processed: set[str] = set()
# => This keeps the modeled rule explicit so its trade-off can be inspected.
for message_id in attempts:
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    if message_id not in processed:
        # => This keeps the modeled rule explicit so its trade-off can be inspected.
        processed.add(message_id)
        # => This keeps the modeled rule explicit so its trade-off can be inspected.
        balance += 10
# => At-least-once transport plus idempotency yields one net effect.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert balance == 10
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(balance)

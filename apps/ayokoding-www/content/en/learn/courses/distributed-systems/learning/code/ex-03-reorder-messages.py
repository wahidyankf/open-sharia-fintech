# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 3."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
sent: list[str] = ["first", "second"]
# => This keeps the modeled rule explicit so its trade-off can be inspected.
arrived: list[str] = ["second", "first"]
# => Arrival order need not equal sender order.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert arrived != sent
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(arrived)

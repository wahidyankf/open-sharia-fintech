"""Runnable artifact for distributed-systems Example 3."""

from __future__ import annotations

sent: list[str] = ["first", "second"]
arrived: list[str] = ["second", "first"]
# => Arrival order need not equal sender order.
assert arrived != sent
print(arrived)

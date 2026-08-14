"""Runnable artifact for distributed-systems Example 66."""

from __future__ import annotations

promised: int = 8
proposal: int = 8
value: str = "x"
accepted: bool = proposal >= promised
# => Phase two accepts only a proposal meeting the promise.
assert accepted and value == "x"
print(accepted)

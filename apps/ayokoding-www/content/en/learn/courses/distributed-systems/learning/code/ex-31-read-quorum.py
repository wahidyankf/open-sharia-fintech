"""Runnable artifact for distributed-systems Example 31."""

from __future__ import annotations

responses: list[str] = ["new"]
required: int = 2
accepted: bool = len(responses) >= required
# => One response cannot satisfy a two-replica read contract.
assert not accepted
print(accepted)

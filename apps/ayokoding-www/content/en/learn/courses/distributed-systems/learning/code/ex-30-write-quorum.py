"""Runnable artifact for distributed-systems Example 30."""

from __future__ import annotations

acks: int = 1
required: int = 2
accepted: bool = acks >= required
# => A below-quorum write cannot report quorum success.
assert not accepted
print(accepted)

"""Runnable artifact for distributed-systems Example 11."""

from __future__ import annotations

receiver: dict[str, int] = {"a": 1, "b": 2}
message: dict[str, int] = {"a": 3, "b": 1}
merged: dict[str, int] = {node: max(receiver[node], message[node]) for node in receiver}
# => Element-wise maximum preserves both causal observations.
assert merged == {"a": 3, "b": 2}
print(merged)

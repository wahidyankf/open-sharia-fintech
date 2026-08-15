# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 11."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
receiver: dict[str, int] = {"a": 1, "b": 2}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
message: dict[str, int] = {"a": 3, "b": 1}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
merged: dict[str, int] = {node: max(receiver[node], message[node]) for node in receiver}
# => Element-wise maximum preserves both causal observations.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert merged == {"a": 3, "b": 2}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(merged)

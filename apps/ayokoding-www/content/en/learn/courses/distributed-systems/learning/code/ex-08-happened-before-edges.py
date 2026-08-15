# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 8."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
edges: set[tuple[str, str]] = {("send", "receive"), ("receive", "apply")}
# => Local and message edges compose a causal history.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert ("send", "receive") in edges and ("receive", "apply") in edges
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(edges)

"""Runnable artifact for distributed-systems Example 8."""

from __future__ import annotations

edges: set[tuple[str, str]] = {("send", "receive"), ("receive", "apply")}
# => Local and message edges compose a causal history.
assert ("send", "receive") in edges and ("receive", "apply") in edges
print(edges)

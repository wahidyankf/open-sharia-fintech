"""Runnable artifact for distributed-systems Example 4."""

from __future__ import annotations

node_a_time: int = 10
node_b_time: int = 9
# => A later real event can have an earlier local clock reading.
assert node_b_time < node_a_time
print((node_a_time, node_b_time))

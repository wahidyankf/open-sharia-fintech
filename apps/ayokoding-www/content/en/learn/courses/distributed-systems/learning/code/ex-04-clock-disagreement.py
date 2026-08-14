# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 4."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
node_a_time: int = 10
# => This keeps the modeled rule explicit so its trade-off can be inspected.
node_b_time: int = 9
# => A later real event can have an earlier local clock reading.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert node_b_time < node_a_time
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print((node_a_time, node_b_time))

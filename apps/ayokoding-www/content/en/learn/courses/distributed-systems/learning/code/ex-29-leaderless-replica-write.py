# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 29."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
replicas: list[dict[str, int]] = [{}, {}, {}]
# => This keeps the modeled rule explicit so its trade-off can be inspected.
for replica in replicas:
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    replica["x"] = 1
# => Direct writes update each reachable replica independently.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert all(replica["x"] == 1 for replica in replicas)
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(replicas)

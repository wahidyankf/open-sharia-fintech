"""Runnable artifact for distributed-systems Example 29."""

from __future__ import annotations

replicas: list[dict[str, int]] = [{}, {}, {}]
for replica in replicas:
    replica["x"] = 1
# => Direct writes update each reachable replica independently.
assert all(replica["x"] == 1 for replica in replicas)
print(replicas)

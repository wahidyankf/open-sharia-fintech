# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 17."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
replicas: list[dict[str, str]] = [{"value": "old"}, {"value": "new"}]
# => This keeps the modeled rule explicit so its trade-off can be inspected.
replicas[0]["value"] = replicas[1]["value"]
# => Propagation makes temporarily divergent replicas converge.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert {replica["value"] for replica in replicas} == {"new"}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(replicas)

"""Runnable artifact for distributed-systems Example 17."""

from __future__ import annotations

replicas: list[dict[str, str]] = [{"value": "old"}, {"value": "new"}]
replicas[0]["value"] = replicas[1]["value"]
# => Propagation makes temporarily divergent replicas converge.
assert {replica["value"] for replica in replicas} == {"new"}
print(replicas)

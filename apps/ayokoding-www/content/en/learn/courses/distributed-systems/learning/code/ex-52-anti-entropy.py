# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 52."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
left: set[str] = {"a", "b"}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
right: set[str] = {"b", "c"}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
merged: set[str] = left | right
# => A commutative merge lets replicas exchange missing observations.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert merged == {"a", "b", "c"}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(sorted(merged))

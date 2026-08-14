# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 12."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
before: dict[str, int] = {"a": 1, "b": 0}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
after: dict[str, int] = {"a": 2, "b": 1}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
dominates: bool = (
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    all(before[node] <= after[node] for node in before) and before != after
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
)
# => Strict vector dominance represents happened-before.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert dominates
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(dominates)

# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 36."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
left: dict[str, int] = {"a": 2, "b": 0}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
right: dict[str, int] = {"a": 1, "b": 1}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
comparable: bool = all(left[k] <= right[k] for k in left) or all(
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    right[k] <= left[k]
    for k in left
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
)
# => Incomparable vectors preserve a conflict for policy to resolve.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert not comparable
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print("conflict")

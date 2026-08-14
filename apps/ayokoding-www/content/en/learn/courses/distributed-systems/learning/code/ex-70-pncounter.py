# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 70."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
increments: dict[str, int] = {"a": 5}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
decrements: dict[str, int] = {"a": 2}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
value: int = sum(increments.values()) - sum(decrements.values())
# => Two grow-only components represent a counter that can decrease.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert value == 3
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(value)

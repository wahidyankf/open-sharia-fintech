"""Runnable artifact for distributed-systems Example 70."""

from __future__ import annotations

increments: dict[str, int] = {"a": 5}
decrements: dict[str, int] = {"a": 2}
value: int = sum(increments.values()) - sum(decrements.values())
# => Two grow-only components represent a counter that can decrease.
assert value == 3
print(value)

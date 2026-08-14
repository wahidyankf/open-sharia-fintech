# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 14."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
scalar_order: list[tuple[int, str]] = sorted([(2, "a"), (2, "b")])
# => This keeps the modeled rule explicit so its trade-off can be inspected.
vector_a: dict[str, int] = {"a": 1, "b": 0}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
vector_b: dict[str, int] = {"a": 0, "b": 1}
# => Scalar ordering can hide vector-visible concurrency.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert scalar_order and vector_a != vector_b
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(scalar_order)

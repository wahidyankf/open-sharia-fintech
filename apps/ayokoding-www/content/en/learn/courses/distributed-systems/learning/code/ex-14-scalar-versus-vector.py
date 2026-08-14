"""Runnable artifact for distributed-systems Example 14."""

from __future__ import annotations

scalar_order: list[tuple[int, str]] = sorted([(2, "a"), (2, "b")])
vector_a: dict[str, int] = {"a": 1, "b": 0}
vector_b: dict[str, int] = {"a": 0, "b": 1}
# => Scalar ordering can hide vector-visible concurrency.
assert scalar_order and vector_a != vector_b
print(scalar_order)

"""Runnable artifact for distributed-systems Example 73."""

from __future__ import annotations

a: set[str] = {"a"}
b: set[str] = {"b"}
c: set[str] = {"c"}
# => Associative merge reaches the same state under different exchange orders.
assert (a | b) | c == a | (b | c)
print(sorted((a | b) | c))

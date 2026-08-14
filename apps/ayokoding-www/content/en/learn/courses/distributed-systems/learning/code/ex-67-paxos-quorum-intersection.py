"""Runnable artifact for distributed-systems Example 67."""

from __future__ import annotations

first_quorum: set[str] = {"a", "b"}
second_quorum: set[str] = {"b", "c"}
intersection: set[str] = first_quorum & second_quorum
# => The shared acceptor carries prior acceptance information forward.
assert intersection == {"b"}
print(sorted(intersection))

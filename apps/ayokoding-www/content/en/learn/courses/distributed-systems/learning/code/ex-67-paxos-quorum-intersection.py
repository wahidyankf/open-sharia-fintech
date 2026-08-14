# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 67."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
first_quorum: set[str] = {"a", "b"}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
second_quorum: set[str] = {"b", "c"}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
intersection: set[str] = first_quorum & second_quorum
# => The shared acceptor carries prior acceptance information forward.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert intersection == {"b"}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(sorted(intersection))

# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 73."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
a: set[str] = {"a"}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
b: set[str] = {"b"}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
c: set[str] = {"c"}
# => Associative merge reaches the same state under different exchange orders.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert (a | b) | c == a | (b | c)
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(sorted((a | b) | c))

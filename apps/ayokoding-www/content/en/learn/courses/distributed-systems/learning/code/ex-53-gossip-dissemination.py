# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 53."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
informed: set[str] = {"a"}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
informed.update({"b", "c", "d"})
# => A completed gossip round can spread one update to each peer here.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert informed == {"a", "b", "c", "d"}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(sorted(informed))

"""Runnable artifact for distributed-systems Example 53."""

from __future__ import annotations

informed: set[str] = {"a"}
informed.update({"b", "c", "d"})
# => A completed gossip round can spread one update to each peer here.
assert informed == {"a", "b", "c", "d"}
print(sorted(informed))

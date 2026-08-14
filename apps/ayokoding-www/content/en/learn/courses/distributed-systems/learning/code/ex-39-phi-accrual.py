"""Runnable artifact for distributed-systems Example 39."""

from __future__ import annotations

elapsed: int = 30
expected_interval: int = 10
phi: float = elapsed / expected_interval
# => Suspicion increases continuously as silence spans expected intervals.
assert phi == 3.0
print(phi)

# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 39."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
elapsed: int = 30
# => This keeps the modeled rule explicit so its trade-off can be inspected.
expected_interval: int = 10
# => This keeps the modeled rule explicit so its trade-off can be inspected.
phi: float = elapsed / expected_interval
# => Suspicion increases continuously as silence spans expected intervals.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert phi == 3.0
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(phi)

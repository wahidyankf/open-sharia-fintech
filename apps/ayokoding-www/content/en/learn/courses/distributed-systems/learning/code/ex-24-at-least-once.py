# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 24."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
deliveries: list[str] = ["reserve", "reserve"]
# => Retrying after an uncertain acknowledgement can duplicate delivery.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert len(deliveries) == 2
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(deliveries)

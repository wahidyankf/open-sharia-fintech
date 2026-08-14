"""Runnable artifact for distributed-systems Example 24."""

from __future__ import annotations

deliveries: list[str] = ["reserve", "reserve"]
# => Retrying after an uncertain acknowledgement can duplicate delivery.
assert len(deliveries) == 2
print(deliveries)

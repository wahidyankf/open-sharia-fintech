# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 83."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from dataclasses import dataclass


# => This keeps the modeled rule explicit so its trade-off can be inspected.
@dataclass(frozen=True)
# => This keeps the modeled rule explicit so its trade-off can be inspected.
class Lease:
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    expires_at: int


# => This keeps the modeled rule explicit so its trade-off can be inspected.
registry: dict[str, Lease] = {"/services/orders/node-a": Lease(expires_at=10)}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
now: int = 11
# => This keeps the modeled rule explicit so its trade-off can be inspected.
live_services: list[str] = [
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    key
    for key, lease in registry.items()
    if now < lease.expires_at
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
]
# => A missed renewal removes the lease-backed service from discovery.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert live_services == []
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(live_services)

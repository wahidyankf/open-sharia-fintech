"""Runnable artifact for distributed-systems Example 83."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Lease:
    expires_at: int


registry: dict[str, Lease] = {"/services/orders/node-a": Lease(expires_at=10)}
now: int = 11
live_services: list[str] = [
    key for key, lease in registry.items() if now < lease.expires_at
]
# => A missed renewal removes the lease-backed service from discovery.
assert live_services == []
print(live_services)

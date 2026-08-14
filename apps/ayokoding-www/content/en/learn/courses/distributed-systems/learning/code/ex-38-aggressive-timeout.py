"""Runnable artifact for distributed-systems Example 38."""

from __future__ import annotations

observed_delay_ms: int = 120
timeout_ms: int = 100
suspect: bool = observed_delay_ms > timeout_ms
# => A live late response can produce a false suspicion.
assert suspect
print(suspect)

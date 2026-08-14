"""Runnable artifact for distributed-systems Example 54."""

from __future__ import annotations

now: int = 11
expires_at: int = 10
valid: bool = now < expires_at
# => Authority ends at lease expiry even if the holder keeps acting.
assert not valid
print(valid)

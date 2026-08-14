# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 54."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
now: int = 11
# => This keeps the modeled rule explicit so its trade-off can be inspected.
expires_at: int = 10
# => This keeps the modeled rule explicit so its trade-off can be inspected.
valid: bool = now < expires_at
# => Authority ends at lease expiry even if the holder keeps acting.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert not valid
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(valid)

# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 38."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
observed_delay_ms: int = 120
# => This keeps the modeled rule explicit so its trade-off can be inspected.
timeout_ms: int = 100
# => This keeps the modeled rule explicit so its trade-off can be inspected.
suspect: bool = observed_delay_ms > timeout_ms
# => A live late response can produce a false suspicion.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert suspect
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(suspect)

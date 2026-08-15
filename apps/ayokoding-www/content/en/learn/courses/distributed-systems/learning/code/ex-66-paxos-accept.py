# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 66."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
promised: int = 8
# => This keeps the modeled rule explicit so its trade-off can be inspected.
proposal: int = 8
# => This keeps the modeled rule explicit so its trade-off can be inspected.
value: str = "x"
# => This keeps the modeled rule explicit so its trade-off can be inspected.
accepted: bool = proposal >= promised
# => Phase two accepts only a proposal meeting the promise.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert accepted and value == "x"
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(accepted)

# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 37."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
missed: int = 3
# => This keeps the modeled rule explicit so its trade-off can be inspected.
threshold: int = 3
# => This keeps the modeled rule explicit so its trade-off can be inspected.
suspect: bool = missed >= threshold
# => Silence reaches a policy threshold, not physical proof of failure.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert suspect
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(suspect)

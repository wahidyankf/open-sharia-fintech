# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 46."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
missed: int = 4
# => This keeps the modeled rule explicit so its trade-off can be inspected.
threshold: int = 3
# => This keeps the modeled rule explicit so its trade-off can be inspected.
replace_peer: bool = missed >= threshold
# => Progress comes from an explicit, fallible timeout assumption.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert replace_peer
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(replace_peer)

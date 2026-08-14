# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 49."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
synchronous_network: bool = True
# => This keeps the modeled rule explicit so its trade-off can be inspected.
precommitted: bool = True
# => This keeps the modeled rule explicit so its trade-off can be inspected.
can_finish: bool = synchronous_network and precommitted
# => Three-phase progress depends on bounded communication.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert can_finish
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(can_finish)

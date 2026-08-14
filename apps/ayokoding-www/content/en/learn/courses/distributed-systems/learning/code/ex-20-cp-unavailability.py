# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 20."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
quorum_available: bool = False
# => This keeps the modeled rule explicit so its trade-off can be inspected.
accepted: bool = quorum_available
# => Refusal preserves the agreement promise when quorum is absent.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert not accepted
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(accepted)

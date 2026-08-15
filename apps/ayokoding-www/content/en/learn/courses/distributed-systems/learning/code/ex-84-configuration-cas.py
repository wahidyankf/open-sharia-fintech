# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 84."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
current_revision: int = 12
# => This keeps the modeled rule explicit so its trade-off can be inspected.
writer_revision: int = 11
# => This keeps the modeled rule explicit so its trade-off can be inspected.
accepted: bool = writer_revision == current_revision
# => A stale compare-and-swap is rejected instead of losing a newer update.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert not accepted
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(accepted)

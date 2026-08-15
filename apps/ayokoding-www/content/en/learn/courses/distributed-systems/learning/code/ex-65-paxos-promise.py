# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 65."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
promised: int = 7
# => This keeps the modeled rule explicit so its trade-off can be inspected.
prepare: int = 8
# => This keeps the modeled rule explicit so its trade-off can be inspected.
accepted: bool = prepare > promised
# => A higher prepare advances the promise and excludes older proposals.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert accepted
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(accepted)

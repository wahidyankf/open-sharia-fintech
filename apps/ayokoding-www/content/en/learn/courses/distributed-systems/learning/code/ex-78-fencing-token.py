# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 78."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
last_accepted: int = 9
# => This keeps the modeled rule explicit so its trade-off can be inspected.
incoming: int = 8
# => This keeps the modeled rule explicit so its trade-off can be inspected.
accepted: bool = incoming > last_accepted
# => The protected resource rejects superseded authority itself.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert not accepted
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(accepted)

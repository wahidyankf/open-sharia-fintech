# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 2."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
sent: str = "reserve"
# => This keeps the modeled rule explicit so its trade-off can be inspected.
delivered: list[str] = []
# => This keeps the modeled rule explicit so its trade-off can be inspected.
drop: bool = True
# => This keeps the modeled rule explicit so its trade-off can be inspected.
if not drop:
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    delivered.append(sent)
# => A local send does not prove remote execution.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert delivered == []
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(delivered)

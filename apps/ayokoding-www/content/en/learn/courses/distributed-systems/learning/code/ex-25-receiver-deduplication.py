# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 25."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
seen: set[str] = set()
# => This keeps the modeled rule explicit so its trade-off can be inspected.
applied: list[str] = []
# => This keeps the modeled rule explicit so its trade-off can be inspected.
for message_id in ["m-1", "m-1"]:
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    if message_id not in seen:
        # => This keeps the modeled rule explicit so its trade-off can be inspected.
        seen.add(message_id)
        # => This keeps the modeled rule explicit so its trade-off can be inspected.
        applied.append(message_id)
# => Stored identity lets only the first delivery change state.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert applied == ["m-1"]
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(applied)

# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 23."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
lossy_send_succeeds: bool = False
# => This keeps the modeled rule explicit so its trade-off can be inspected.
received: list[str] = []
# => This keeps the modeled rule explicit so its trade-off can be inspected.
if lossy_send_succeeds:
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    received.append("charge")
# => No retry means loss is possible but duplicates are not.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert received == []
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(received)

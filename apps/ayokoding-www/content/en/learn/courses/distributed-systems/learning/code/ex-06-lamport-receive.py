# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 6."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
receiver_clock: int = 3
# => This keeps the modeled rule explicit so its trade-off can be inspected.
message_clock: int = 7
# => This keeps the modeled rule explicit so its trade-off can be inspected.
receiver_clock = max(receiver_clock, message_clock) + 1
# => Receiving advances past both local and message time.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert receiver_clock == 8
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(receiver_clock)

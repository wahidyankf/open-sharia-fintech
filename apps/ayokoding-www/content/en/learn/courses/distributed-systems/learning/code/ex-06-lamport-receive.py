"""Runnable artifact for distributed-systems Example 6."""

from __future__ import annotations

receiver_clock: int = 3
message_clock: int = 7
receiver_clock = max(receiver_clock, message_clock) + 1
# => Receiving advances past both local and message time.
assert receiver_clock == 8
print(receiver_clock)

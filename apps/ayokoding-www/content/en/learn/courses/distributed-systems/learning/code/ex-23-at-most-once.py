"""Runnable artifact for distributed-systems Example 23."""

from __future__ import annotations

lossy_send_succeeds: bool = False
received: list[str] = []
if lossy_send_succeeds:
    received.append("charge")
# => No retry means loss is possible but duplicates are not.
assert received == []
print(received)

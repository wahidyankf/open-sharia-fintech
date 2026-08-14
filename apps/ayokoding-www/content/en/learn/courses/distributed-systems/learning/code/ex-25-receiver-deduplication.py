"""Runnable artifact for distributed-systems Example 25."""

from __future__ import annotations

seen: set[str] = set()
applied: list[str] = []
for message_id in ["m-1", "m-1"]:
    if message_id not in seen:
        seen.add(message_id)
        applied.append(message_id)
# => Stored identity lets only the first delivery change state.
assert applied == ["m-1"]
print(applied)

# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 15."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
applied: list[str] = ["create"]
# => This keeps the modeled rule explicit so its trade-off can be inspected.
buffer: list[str] = ["rename"]
# => This keeps the modeled rule explicit so its trade-off can be inspected.
if "create" in applied:
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    applied.extend(buffer)
# => A dependency gate releases the causal successor only after its cause.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert applied == ["create", "rename"]
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(applied)

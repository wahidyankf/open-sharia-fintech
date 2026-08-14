"""Runnable artifact for distributed-systems Example 15."""

from __future__ import annotations

applied: list[str] = ["create"]
buffer: list[str] = ["rename"]
if "create" in applied:
    applied.extend(buffer)
# => A dependency gate releases the causal successor only after its cause.
assert applied == ["create", "rename"]
print(applied)

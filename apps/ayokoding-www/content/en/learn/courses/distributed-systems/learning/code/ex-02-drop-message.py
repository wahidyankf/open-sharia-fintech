"""Runnable artifact for distributed-systems Example 2."""

from __future__ import annotations

sent: str = "reserve"
delivered: list[str] = []
drop: bool = True
if not drop:
    delivered.append(sent)
# => A local send does not prove remote execution.
assert delivered == []
print(delivered)

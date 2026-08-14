"""Runnable artifact for distributed-systems Example 78."""

from __future__ import annotations

last_accepted: int = 9
incoming: int = 8
accepted: bool = incoming > last_accepted
# => The protected resource rejects superseded authority itself.
assert not accepted
print(accepted)

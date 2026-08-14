"""Runnable artifact for distributed-systems Example 84."""

from __future__ import annotations

current_revision: int = 12
writer_revision: int = 11
accepted: bool = writer_revision == current_revision
# => A stale compare-and-swap is rejected instead of losing a newer update.
assert not accepted
print(accepted)

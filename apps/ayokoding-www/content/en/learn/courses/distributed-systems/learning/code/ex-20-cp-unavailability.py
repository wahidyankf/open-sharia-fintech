"""Runnable artifact for distributed-systems Example 20."""

from __future__ import annotations

quorum_available: bool = False
accepted: bool = quorum_available
# => Refusal preserves the agreement promise when quorum is absent.
assert not accepted
print(accepted)

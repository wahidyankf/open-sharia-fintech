"""Runnable artifact for distributed-systems Example 49."""

from __future__ import annotations

synchronous_network: bool = True
precommitted: bool = True
can_finish: bool = synchronous_network and precommitted
# => Three-phase progress depends on bounded communication.
assert can_finish
print(can_finish)

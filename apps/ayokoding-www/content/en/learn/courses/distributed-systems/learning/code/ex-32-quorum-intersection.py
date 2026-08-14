"""Runnable artifact for distributed-systems Example 32."""

from __future__ import annotations

members: int = 3
read_quorum: int = 2
write_quorum: int = 2
# => R + W > N forces completed reads and writes to overlap.
assert read_quorum + write_quorum > members
print("intersects")

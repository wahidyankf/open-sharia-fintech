"""Runnable artifact for distributed-systems Example 42."""

from __future__ import annotations

log: list[str] = ["set:x=1"]
log.append("set:x=2")
# => Later state transitions add history rather than rewrite committed positions.
assert log == ["set:x=1", "set:x=2"]
print(log)

# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 42."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
log: list[str] = ["set:x=1"]
# => This keeps the modeled rule explicit so its trade-off can be inspected.
log.append("set:x=2")
# => Later state transitions add history rather than rewrite committed positions.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert log == ["set:x=1", "set:x=2"]
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(log)

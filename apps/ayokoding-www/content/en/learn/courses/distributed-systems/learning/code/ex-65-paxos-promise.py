"""Runnable artifact for distributed-systems Example 65."""

from __future__ import annotations

promised: int = 7
prepare: int = 8
accepted: bool = prepare > promised
# => A higher prepare advances the promise and excludes older proposals.
assert accepted
print(accepted)

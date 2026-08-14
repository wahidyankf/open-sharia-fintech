"""Runnable artifact for distributed-systems Example 75."""

from __future__ import annotations

phases: list[str] = ["pre-prepare", "prepare", "commit"]
# => The sequence identifies the evidence-gathering rounds for one request.
assert phases[-1] == "commit"
print(phases)

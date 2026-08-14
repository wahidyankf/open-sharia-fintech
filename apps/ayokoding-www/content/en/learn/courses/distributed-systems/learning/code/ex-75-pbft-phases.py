# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 75."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
phases: list[str] = ["pre-prepare", "prepare", "commit"]
# => The sequence identifies the evidence-gathering rounds for one request.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert phases[-1] == "commit"
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(phases)

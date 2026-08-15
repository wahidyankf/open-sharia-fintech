# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 47."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
votes: list[str] = ["yes", "yes"]
# => This keeps the modeled rule explicit so its trade-off can be inspected.
decision: str = "commit" if all(vote == "yes" for vote in votes) else "abort"
# => The coordinator issues one all-or-nothing decision after prepares.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert decision == "commit"
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(decision)

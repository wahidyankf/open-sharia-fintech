"""Runnable artifact for distributed-systems Example 47."""

from __future__ import annotations

votes: list[str] = ["yes", "yes"]
decision: str = "commit" if all(vote == "yes" for vote in votes) else "abort"
# => The coordinator issues one all-or-nothing decision after prepares.
assert decision == "commit"
print(decision)

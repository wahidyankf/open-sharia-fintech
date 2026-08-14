"""Runnable artifact for distributed-systems Example 76."""

from __future__ import annotations

completed: list[str] = ["reserve inventory"]
failed: bool = True
if failed:
    completed.append("release inventory")
# => Compensation adds a new local action; it is not a global rollback.
assert completed[-1] == "release inventory"
print(completed)

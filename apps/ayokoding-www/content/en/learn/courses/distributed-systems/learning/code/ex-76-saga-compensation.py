# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 76."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
completed: list[str] = ["reserve inventory"]
# => This keeps the modeled rule explicit so its trade-off can be inspected.
failed: bool = True
# => This keeps the modeled rule explicit so its trade-off can be inspected.
if failed:
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    completed.append("release inventory")
# => Compensation adds a new local action; it is not a global rollback.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert completed[-1] == "release inventory"
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(completed)

# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 16."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
register: dict[str, str | None] = {"value": None}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
register["value"] = "paid"
# => A later read observes the completed authoritative write.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert register["value"] == "paid"
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(register["value"])

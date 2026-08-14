"""Runnable artifact for distributed-systems Example 16."""

from __future__ import annotations

register: dict[str, str | None] = {"value": None}
register["value"] = "paid"
# => A later read observes the completed authoritative write.
assert register["value"] == "paid"
print(register["value"])

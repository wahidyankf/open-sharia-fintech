# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 82."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
candidates: list[str] = ["member-0001", "member-0002", "member-0003"]
# => This keeps the modeled rule explicit so its trade-off can be inspected.
leader: str = min(candidates)
# => This keeps the modeled rule explicit so its trade-off can be inspected.
predecessor_watch: dict[str, str] = {
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    candidates[index]: candidates[index - 1]
    for index in range(1, len(candidates))
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
}
# => Each nonleader watches only its predecessor, avoiding a herd watch.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert leader == "member-0001"
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert predecessor_watch == {"member-0002": "member-0001", "member-0003": "member-0002"}
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print((leader, predecessor_watch))

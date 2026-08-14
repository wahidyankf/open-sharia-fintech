"""Runnable artifact for distributed-systems Example 82."""

from __future__ import annotations

candidates: list[str] = ["member-0001", "member-0002", "member-0003"]
leader: str = min(candidates)
predecessor_watch: dict[str, str] = {
    candidates[index]: candidates[index - 1] for index in range(1, len(candidates))
}
# => Each nonleader watches only its predecessor, avoiding a herd watch.
assert leader == "member-0001"
assert predecessor_watch == {"member-0002": "member-0001", "member-0003": "member-0002"}
print((leader, predecessor_watch))

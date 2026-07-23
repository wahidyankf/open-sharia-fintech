from collections.abc import Callable
from typing import TypedDict


class Task(TypedDict):
    id: int
    status: str
    priority: int


class Page(TypedDict):  # => co-19: a typed pagination envelope -- items, total, and a next-page cursor
    items: list[Task]
    total: int
    next_offset: int | None


# => co-20: a small allowlist of sortable fields, each with an explicit typed accessor (never eval()'d)
SORT_KEYS: dict[str, Callable[[Task], int]] = {"priority": lambda t: t["priority"]}


def list_tasks(  # => co-19/co-20: pagination + filter + sort composed in ONE query-shaping function
    tasks: list[Task],
    status: str | None,
    sort_by: str | None,
    limit: int,
    offset: int,
) -> Page:
    filtered = [t for t in tasks if status is None or t["status"] == status]  # => co-20: filter step first
    if sort_by is not None:  # => co-20: sort step second, over the ALREADY-filtered set
        filtered = sorted(filtered, key=SORT_KEYS[sort_by])
    page = filtered[offset : offset + limit]  # => co-19: pagination step LAST, over the filtered+sorted set
    return {  # => co-19: pagination metadata alongside the page itself
        "items": page,
        "total": len(filtered),  # => co-19: total reflects the FILTERED count, not the whole table
        "next_offset": offset + limit if offset + limit < len(filtered) else None,
    }


tasks: list[Task] = [
    {"id": 1, "status": "open", "priority": 3},
    {"id": 2, "status": "open", "priority": 1},
    {"id": 3, "status": "done", "priority": 2},
    {"id": 4, "status": "open", "priority": 2},
]

page1 = list_tasks(tasks, status="open", sort_by="priority", limit=2, offset=0)  # => co-19/co-20: all 3 combine
page2 = list_tasks(tasks, status="open", sort_by="priority", limit=2, offset=2)  # => the SECOND page

print([t["id"] for t in page1["items"]], page1["total"], page1["next_offset"])  # => Output: [2, 4] 3 2
print([t["id"] for t in page2["items"]], page2["total"], page2["next_offset"])  # => Output: [1] 3 None

assert [t["id"] for t in page1["items"]] == [2, 4]  # => sorted by priority (1, 2) among "open" tasks
assert page1["total"] == 3  # => co-19: 3 total open tasks, even though only 2 are on this page
assert page1["next_offset"] == 2  # => co-19: a next page exists
assert page2["next_offset"] is None  # => co-19: this page reaches the end of the filtered set
print("kata-19 OK")

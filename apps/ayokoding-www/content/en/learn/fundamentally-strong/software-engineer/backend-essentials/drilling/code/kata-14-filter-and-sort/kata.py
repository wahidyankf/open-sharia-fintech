from collections.abc import Callable
from typing import TypedDict


class Task(TypedDict):
    id: int
    status: str
    priority: str


FILTER_KEYS: dict[str, Callable[[Task], str]] = {  # => co-20: an allowlist -- never eval() a raw field name
    "status": lambda t: t["status"],
    "priority": lambda t: t["priority"],
}
SORT_KEYS: dict[str, Callable[[Task], str]] = FILTER_KEYS  # => same typed accessors double as sort keys


def filter_and_sort(tasks: list[Task], filters: dict[str, str], sort_key: str | None) -> list[Task]:  # => co-20: query-param-like filters narrow the list, an optional sort orders it
    result = [  # => co-20: AND semantics -- a row must match EVERY supplied filter, not just one
        task for task in tasks if all(FILTER_KEYS[field](task) == value for field, value in filters.items())
    ]
    if sort_key is not None:  # => co-20: sort is optional -- absent means "keep insertion order"
        result = sorted(result, key=SORT_KEYS[sort_key])  # => Timsort: stable, O(n log n)
    return result


tasks: list[Task] = [
    {"id": 1, "status": "open", "priority": "high"},
    {"id": 2, "status": "done", "priority": "low"},
    {"id": 3, "status": "done", "priority": "high"},
    {"id": 4, "status": "open", "priority": "low"},
]

done_only = filter_and_sort(tasks, {"status": "done"}, None)  # => single filter, no sort
done_high = filter_and_sort(tasks, {"status": "done", "priority": "high"}, None)  # => co-20: two filters, AND'd
sorted_by_priority = filter_and_sort(tasks, {}, "priority")  # => no filter at all, just a sort

print([t["id"] for t in done_only])  # => Output: [2, 3]
print([t["id"] for t in done_high])  # => Output: [3]
print([t["id"] for t in sorted_by_priority])  # => Output: [1, 3, 2, 4] -- alphabetical: high, high, low, low

assert [t["id"] for t in done_only] == [2, 3]
assert [t["id"] for t in done_high] == [3]  # => id 2 is done but low priority -- excluded by the AND
assert [t["id"] for t in sorted_by_priority] == [1, 3, 2, 4]
print("kata-14 OK")

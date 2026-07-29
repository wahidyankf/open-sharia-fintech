# pyright: strict
"""Example 25: A Consistent Pagination Envelope. (co-29)

Every list endpoint wraps its page the SAME way: `data` (the items),
`has_more` (whether another page exists), and `next_cursor` (how to get it)
-- one shape, reused regardless of which resource is being paged.
"""

from dataclasses import dataclass, field  # => field: default_factory for the data list
from typing import Any  # => an item's own shape stays generic here


@dataclass  # => co-29: the one envelope shape every paged endpoint returns
class Page:  # => co-29: data + has_more + next_cursor, nothing more, nothing less
    data: list[Any] = field(default_factory=list[Any])  # => the page's own items
    has_more: bool = False  # => whether another page exists beyond this one
    next_cursor: int | None = None  # => how to fetch that next page, or None if there is none


ARTICLES = [{"id": i} for i in range(1, 11)]  # => 10 items


def _index_of_cursor(items: list[dict[str, int]], cursor: int) -> int:  # => co-29: finds the cursor's own row
    for i, item in enumerate(items):  # => co-29: scans for the exact row the cursor names
        if item["id"] == cursor:  # => co-29: found it -- this row is what the cursor points at
            return i + 1  # => co-29: resumes ONE PAST the cursor, never re-showing that row
    raise ValueError(f"cursor {cursor} not found")  # => co-29: an unknown cursor is a genuine error


def paginate(items: list[dict[str, int]], cursor: int | None, limit: int) -> Page:  # => co-29 builder
    # => co-29: builds the SAME three-field envelope regardless of the underlying resource
    start = 0 if cursor is None else _index_of_cursor(items, cursor)  # => no cursor -> start at the beginning
    window = items[start : start + limit]  # => this page's own slice of items
    has_more = start + limit < len(items)  # => co-29: True while items remain beyond this window
    next_cursor = window[-1]["id"] if window and has_more else None  # => None on the LAST page
    return Page(data=window, has_more=has_more, next_cursor=next_cursor)  # => the one envelope shape


page_1 = paginate(ARTICLES, cursor=None, limit=4)  # => first page
ids_1 = [d["id"] for d in page_1.data]  # => extracts just the ids, for a compact printed line
print(f"page 1: data={ids_1}, has_more={page_1.has_more}, next_cursor={page_1.next_cursor}")
# => Output: data=[1,2,3,4], has_more=True, next_cursor=4

page_3 = paginate(ARTICLES, cursor=8, limit=4)  # => the LAST page (items 9, 10 only)
ids_3 = [d["id"] for d in page_3.data]  # => extracts just the ids, for a compact printed line
# => ids_3 is [9, 10] -- fewer than `limit`, one of the two signals the LAST page is reached
print(f"page 3: data={ids_3}, has_more={page_3.has_more}, next_cursor={page_3.next_cursor}")
# => Output: data=[9,10], has_more=False, next_cursor=None -- co-29 signals "the end"

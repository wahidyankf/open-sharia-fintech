# pyright: strict
"""Example 13: Cursor Pagination -- resume after a key. (co-05)

A cursor encodes a position IN THE DATA (the last-seen item's sort key) and
the next page resumes with `WHERE id > cursor`. This avoids the fetch-and-
discard cost and is stable under concurrent inserts. Stripe's API calls this
`starting_after`. Source: Stripe pagination docs; "Use The Index, Luke".
"""

from dataclasses import dataclass  # => a small typed response record for a page


@dataclass  # => co-05: a page of items plus the cursor to fetch the next page
class Page:
    data: list[int]  # => the ids on THIS page
    next_cursor: int | None  # => the last id on this page, or None when the end is reached


ROWS: list[int] = list(range(1, 101))  # => 100 rows, ids 1..100, sorted ascending (the indexed key)


def page_starting_after(starting_after: int | None, limit: int) -> Page:  # => co-05: GET /items?starting_after=<id>
    threshold = 0 if starting_after is None else starting_after  # => None means "from the beginning"
    window = [r for r in ROWS if r > threshold][:limit]  # => co-05: an indexed WHERE on the last-seen key, then LIMIT
    next_cursor = window[-1] if len(window) == limit and window[-1] != ROWS[-1] else None  # => None at the very end
    return Page(data=window, next_cursor=next_cursor)  # => the page + the cursor the NEXT request uses


first = page_starting_after(starting_after=None, limit=10)  # => page 1: ids 1..10
print(f"page 1: first={first.data[0]}, last={first.data[-1]}, next_cursor={first.next_cursor}")  # => Output: 1, 10, 10

second = page_starting_after(starting_after=first.next_cursor, limit=10)  # => resumes right after id 10
print(f"page 2: first={second.data[0]}, last={second.data[-1]}, next_cursor={second.next_cursor}")  # => Output: 11, 20, 20

assert second.data[0] == 11  # => co-05: the next page begins right AFTER the cursor id, no skip cost
assert first.data + second.data == list(range(1, 21))  # => contiguous, no overlap and no gap

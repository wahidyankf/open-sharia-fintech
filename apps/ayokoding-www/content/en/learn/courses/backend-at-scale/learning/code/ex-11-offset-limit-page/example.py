# pyright: strict
"""Example 11: Offset/Limit Pagination -- the correct slice. (co-04)

?offset=20&limit=10 asks the server to SKIP 20 rows and return the NEXT 10.
This example builds the slicing and verifies the correct window (rows 21..30)
comes back. The fetch-and-discard COST of that skip is the subject of Example 12.
"""

from dataclasses import dataclass  # => a small typed response record for a page


@dataclass  # => co-04: a page of items plus a pointer to keep paging
class Page:
    data: list[int]  # => the items on THIS page (their ids)
    offset: int  # => the offset this page started at
    limit: int  # => the limit (count) requested
    total: int  # => the full collection size, so the caller knows if more pages exist


ROWS: list[int] = list(range(1, 101))  # => 100 rows, ids 1..100 -- the collection being paged


def page_offset_limit(offset: int, limit: int) -> Page:  # => co-04: GET /items?offset=20&limit=10
    start = offset  # => the number of rows to SKIP
    window = ROWS[start : start + limit]  # => co-04: the next `limit` rows after skipping `offset`
    return Page(data=window, offset=offset, limit=limit, total=len(ROWS))  # => the page envelope


page = page_offset_limit(offset=20, limit=10)  # => skip 20, take 10 -- rows 21..30
print(f"offset=20, limit=10 -> first={page.data[0]}, last={page.data[-1]}, count={len(page.data)}")  # => Output: 21, 30, 10

first_page = page_offset_limit(offset=0, limit=10)  # => the very first page
print(f"offset=0, limit=10  -> first={first_page.data[0]}, last={first_page.data[-1]}")  # => Output: 1, 10

assert page.data == list(range(21, 31))  # => co-04: exactly rows 21 through 30
assert len(page.data) == page.limit  # => the page respects the requested count

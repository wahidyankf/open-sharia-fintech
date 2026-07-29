# pyright: strict
"""Example 24: Cursor Pagination. (co-17)

A cursor (Stripe's `starting_after`/`ending_before` model) points at the
LAST item seen, not a numeric offset -- the database seeks directly to that
position, with no skipped-and-discarded rows and no drift under concurrent
inserts. This example walks the whole list two pages via `next_cursor`.
"""

ARTICLES = [{"id": i, "title": f"Article {i}"} for i in range(1, 11)]  # => 10 items, ids 1..10


def _index_of_cursor(cursor: int) -> int:  # => co-17: finds the cursor's OWN position directly
    for i, article in enumerate(ARTICLES):  # => co-17: seeks the exact row, no skip-and-discard scan
        if article["id"] == cursor:  # => co-17: found the row the cursor itself points at
            return i + 1  # => co-17: resumes ONE PAST the cursor, never re-showing it
    raise ValueError(f"cursor {cursor} not found")  # => co-17: an unknown cursor is a genuine error


def list_articles_cursor(cursor: int | None, limit: int) -> tuple[list[dict[str, object]], int | None]:
    # => GET /articles?starting_after=&limit= -- cursor: the last id seen, or None for the first page
    start_index = 0 if cursor is None else _index_of_cursor(cursor)  # => no cursor -> start at the beginning
    page = ARTICLES[start_index : start_index + limit]  # => the next `limit` items from that seek point
    next_cursor = page[-1]["id"] if len(page) == limit else None  # => None once the list is exhausted
    return page, next_cursor  # type: ignore[return-value]  # => id is a runtime int, kept as object above


page_1, cursor_1 = list_articles_cursor(cursor=None, limit=4)  # => first page: no cursor yet
# => page_1 holds items with id 1..4; cursor_1 is 4 (type: int)
print(f"page 1: {[a['id'] for a in page_1]}, next_cursor={cursor_1}")  # => Output: [1,2,3,4], cursor=4

page_2, cursor_2 = list_articles_cursor(cursor=cursor_1, limit=4)  # => co-17: seeks from item 4 directly
# => page_2 holds items with id 5..8 -- no rows before item 5 were touched to get here
print(f"page 2: {[a['id'] for a in page_2]}, next_cursor={cursor_2}")  # => Output: [5,6,7,8], cursor=8

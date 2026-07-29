# pyright: strict
"""Example 23: Offset/Limit Pagination. (co-16)

`?offset=&limit=` pages a list by skipping N items, then taking the next M.
It is simple to implement, but every request re-fetches and discards the
skipped rows -- the cost this example makes visible with a counted "fetch."
"""

ARTICLES = [f"Article {i}" for i in range(1, 11)]  # => 10 items total, ids implicit by position
# => ARTICLES is ['Article 1', 'Article 2', ..., 'Article 10'] (type: list[str])

FETCH_COUNT = [0]  # => a mutable counter cell -- tracks how many rows the "database" actually reads


def list_articles_offset(offset: int, limit: int) -> list[str]:  # => GET /articles?offset=&limit=
    for _ in range(offset):  # => co-16: simulates the database SKIPPING each preceding row
        FETCH_COUNT[0] += 1  # => every skipped row is still a read, just a discarded one
    page = ARTICLES[offset : offset + limit]  # => co-16: the actual slice returned to the caller
    FETCH_COUNT[0] += len(page)  # => plus the rows that ARE returned
    return page  # => the requested page of results


page = list_articles_offset(offset=3, limit=3)  # => "skip the first 3, take the next 3"
print(f"page: {page}")  # => Output: ['Article 4', 'Article 5', 'Article 6']
print(f"rows the database touched to produce this page: {FETCH_COUNT[0]}")  # => Output: 6 (co-16)
# => 6 = 3 skipped + 3 returned -- offset pagination pays for rows it never shows the caller

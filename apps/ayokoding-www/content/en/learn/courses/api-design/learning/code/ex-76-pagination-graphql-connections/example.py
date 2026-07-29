# pyright: strict
"""Example 76: Relay-Style Cursor Connections in GraphQL. (co-17, co-24)

The Relay connection spec standardizes GraphQL's OWN cursor pagination
shape (co-17's general cursor idea, Example 8) as `edges` (each wrapping a
`node` plus its own `cursor`) and a `pageInfo` object naming whether more
pages exist -- a fixed, reusable shape every paginated field can share.
"""

from typing import Any  # => a connection is arbitrary nested JSON

ALL_ARTICLES = ["Hello", "World", "GraphQL", "Connections", "Relay"]  # => co-17: 5 items, paged 2 at a time


def build_connection(items: list[str], after_cursor: str | None, page_size: int) -> dict[str, Any]:
    # => co-17/co-24: builds ONE page in the Relay connection shape
    start_index = 0 if after_cursor is None else int(after_cursor) + 1  # => co-17: resumes AFTER the cursor
    page_items = items[start_index : start_index + page_size]  # => co-17: exactly page_size items, or fewer
    edges = [  # => co-24: one edge per item, each carrying its OWN cursor
        {"node": item, "cursor": str(start_index + offset)} for offset, item in enumerate(page_items)
    ]  # => end of edges
    has_next_page = (start_index + page_size) < len(items)  # => co-17: are there MORE items after this page?
    end_cursor = edges[-1]["cursor"] if edges else None  # => co-17: the cursor the NEXT request should resume from
    return {  # => co-24: the standardized Relay connection envelope
        "edges": edges,  # => co-24: REQUIRED -- every item plus its own cursor
        "pageInfo": {"hasNextPage": has_next_page, "endCursor": end_cursor},  # => co-17: pagination metadata
    }  # => end of the connection


page_1 = build_connection(ALL_ARTICLES, after_cursor=None, page_size=2)  # => co-17: the FIRST page, no cursor yet
print(f"page 1: {page_1}")  # => Output: edges for items 0-1, hasNextPage=True

page_2 = build_connection(ALL_ARTICLES, after_cursor=page_1["pageInfo"]["endCursor"], page_size=2)
# => co-17: resumes from where page 1's endCursor left off
print(f"page 2: {page_2}")  # => Output: edges for items 2-3, hasNextPage=True

page_3 = build_connection(ALL_ARTICLES, after_cursor=page_2["pageInfo"]["endCursor"], page_size=2)
# => co-17: the LAST page -- fewer items remain than a full page
# => page_3["pageInfo"]["hasNextPage"] is False and page_3["pageInfo"]["endCursor"] is still set
print(f"page 3: {page_3}")  # => Output: edge for item 4 only, hasNextPage=False -- co-17: end of the list

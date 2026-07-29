# pyright: strict
"""Kata 2 (after): the slice end is offset + limit, a COUNT, not an absolute index."""

ARTICLES: list[str] = [f"Article {i}" for i in range(1, 11)]


def list_articles(offset: int, limit: int) -> list[str]:
    # THE FIX: the end index is offset + limit -- limit is a COUNT of items
    # to return, not an absolute position in the list.
    return ARTICLES[offset : offset + limit]


page_1 = list_articles(offset=0, limit=3)
print(f"page 1 (offset=0, limit=3): {page_1}")

page_2 = list_articles(offset=3, limit=3)
print(f"page 2 (offset=3, limit=3): {page_2}")

page_3 = list_articles(offset=6, limit=3)
print(f"page 3 (offset=6, limit=3): {page_3}")

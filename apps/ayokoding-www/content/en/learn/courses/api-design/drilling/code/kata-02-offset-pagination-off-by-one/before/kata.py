# pyright: strict
"""Kata 2 (before): a slicing bug shrinks every page as the offset grows."""

ARTICLES: list[str] = [f"Article {i}" for i in range(1, 11)]  # 10 articles, "Article 1".."Article 10"


def list_articles(offset: int, limit: int) -> list[str]:
    # THE BUG: articles[offset:limit] treats `limit` as an ABSOLUTE end index,
    # not a COUNT -- the window shrinks (or vanishes) as offset grows past limit.
    return ARTICLES[offset:limit]


page_1 = list_articles(offset=0, limit=3)
print(f"page 1 (offset=0, limit=3): {page_1}")

page_2 = list_articles(offset=3, limit=3)  # intent: the NEXT 3 articles
print(f"page 2 (offset=3, limit=3): {page_2}")  # BUG: empty -- offset(3) >= limit(3)

page_3 = list_articles(offset=6, limit=3)
print(f"page 3 (offset=6, limit=3): {page_3}")  # BUG: still empty

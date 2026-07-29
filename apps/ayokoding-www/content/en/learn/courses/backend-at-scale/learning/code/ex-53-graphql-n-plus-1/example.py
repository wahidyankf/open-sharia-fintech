# pyright: strict
"""Example 53: GraphQL N+1 resolver, then a DataLoader batch. (co-07, co-40)

A naive resolver fetches each item's related author ONE AT A TIME across a
list -- 1 query for the list plus N per-item queries (the N+1 problem). A
DataLoader-style batch collapses all N lookups into ONE bulk query. The query
counter proves the drop. co-40 also names the batching fix for the N+1 query.
"""

from dataclasses import dataclass  # => a typed article record avoids dict[int|str] typing pitfalls

QUERY_COUNT = [0]  # => a mutable counter -- how many queries were issued


@dataclass  # => one article, with a slot to hold the resolved author
class Article:
    id: int  # => the article id
    author_id: int  # => the related author to resolve
    author: str = ""  # => filled in by the resolver (empty until resolved)


def fetch_articles() -> list[Article]:  # => the list query (1 query)
    QUERY_COUNT[0] += 1  # => count it
    return [Article(1, 10), Article(2, 20), Article(3, 30)]  # => 3 articles


def fetch_author_naive(author_id: int) -> str:  # => the NAIVE per-item resolver (1 query EACH)
    QUERY_COUNT[0] += 1  # => count each individual lookup
    return f"Author-{author_id}"  # => the resolved author


def fetch_authors_batch(author_ids: list[int]) -> dict[int, str]:  # => co-07/co-40: the DataLoader-style BATCH (1 query)
    QUERY_COUNT[0] += 1  # => ONE bulk query for ALL the ids
    return {aid: f"Author-{aid}" for aid in author_ids}  # => all authors in one shot


# --- The N+1 pattern: 1 (list) + 3 (one per article) = 4 queries. ---
QUERY_COUNT[0] = 0  # => reset
articles = fetch_articles()  # => 1 query
for a in articles:  # => for EACH article...
    a.author = fetch_author_naive(a.author_id)  # => ...one MORE query (N+1)
n_plus_1 = QUERY_COUNT[0]  # => 1 + 3 = 4
print(f"N+1 resolver: {n_plus_1} queries for {len(articles)} articles")  # => Output: 4

# --- The DataLoader fix: 1 (list) + 1 (batch) = 2 queries. ---
QUERY_COUNT[0] = 0  # => reset
articles = fetch_articles()  # => 1 query
author_ids = [a.author_id for a in articles]  # => collect ALL author ids first
authors = fetch_authors_batch(author_ids)  # => co-07/co-40: ONE bulk query for every id
for a in articles:  # => assign from the pre-fetched batch
    a.author = authors[a.author_id]  # => no per-item query
batched = QUERY_COUNT[0]  # => 1 + 1 = 2
print(f"DataLoader batch: {batched} queries for {len(articles)} articles")  # => Output: 2

assert n_plus_1 == 4 and batched == 2  # => co-07/co-40: N+1 collapsed from 4 to a constant 2

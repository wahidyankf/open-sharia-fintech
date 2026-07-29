# pyright: strict
"""Example 61: An N+1 Resolver, Then a DataLoader Batch. (co-25)

Resolving each article's author with its OWN separate lookup means N
articles cost N+1 queries (1 for articles, N for authors) -- batching all
N author lookups into ONE call (the DataLoader pattern) collapses that back
down to 2 queries total, regardless of N.
"""

ARTICLES = [  # => co-25: 3 articles, each referencing an author by id
    {"id": "1", "author_id": "a1"},  # => article 1, written by author a1
    {"id": "2", "author_id": "a2"},  # => article 2, written by author a2
    {"id": "3", "author_id": "a1"},  # => article 3, ALSO written by author a1
]  # => end of ARTICLES
AUTHORS = {"a1": "Ada", "a2": "Grace"}  # => co-25: the underlying author store

QUERY_COUNT = [0]  # => a mutable counter cell -- counts every simulated "database" call


def fetch_author_naive(author_id: str) -> str:  # => co-25: the N+1 resolver -- one call PER article
    QUERY_COUNT[0] += 1  # => co-25: every single call increments the counter
    return AUTHORS[author_id]  # => the author's name, fetched one at a time


QUERY_COUNT[0] = 0  # => reset before measuring the naive path
naive_results = [fetch_author_naive(article["author_id"]) for article in ARTICLES]  # => co-25: 3 separate calls
# => naive_results is ['Ada', 'Grace', 'Ada'] -- author "a1" was queried TWICE, redundantly
print(f"naive results: {naive_results}, query count: {QUERY_COUNT[0]}")  # => Output: 3 names, 3 queries


def fetch_authors_batched(author_ids: list[str]) -> dict[str, str]:  # => co-25: the DataLoader-style batch
    QUERY_COUNT[0] += 1  # => co-25: exactly ONE call, regardless of how many ids are in the batch
    unique_ids = set(author_ids)  # => co-25: deduplicates repeated ids (a1 appears twice above)
    return {author_id: AUTHORS[author_id] for author_id in unique_ids}  # => one lookup covering every id


QUERY_COUNT[0] = 0  # => reset before measuring the batched path
all_author_ids = [article["author_id"] for article in ARTICLES]  # => co-25: collects every id UP FRONT
author_map = fetch_authors_batched(all_author_ids)  # => co-25: ONE call resolves all three articles' authors
batched_results = [author_map[a_id] for a_id in all_author_ids]  # => maps each article back to its author
# => batched_results == naive_results, but QUERY_COUNT[0] is 1, not 3 -- same answer, 1/3 the queries
print(f"batched results: {batched_results}, query count: {QUERY_COUNT[0]}")  # => Output: same 3 names, 1 query

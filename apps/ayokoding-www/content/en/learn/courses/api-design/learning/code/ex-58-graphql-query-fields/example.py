# pyright: strict
"""Example 58: A Client Selects Exactly the Fields It Needs. (co-24)

The caller's own query names the specific fields it wants, and a minimal
executor returns ONLY those fields -- the opposite of REST's fixed response
shape (Example 1), where the server alone decides what comes back.
"""

ARTICLE_DATA = {  # => co-24: the FULL underlying record, before any field selection
    "id": "1",  # => always present regardless of what the client asked for
    "title": "Hello, API Design",  # => a field a caller might select
    "body": "A very long body...",  # => a field a caller might choose NOT to select
    "views": 42,  # => another field a caller might choose NOT to select
}  # => end of ARTICLE_DATA


def execute_query(requested_fields: list[str]) -> dict[str, object]:  # => co-24: a minimal executor
    return {field: ARTICLE_DATA[field] for field in requested_fields if field in ARTICLE_DATA}
    # => co-24: returns ONLY the fields the client's own query named


small_query = execute_query(["id", "title"])  # => a client that only needs id and title
print(f"small query: {small_query}")  # => Output: {'id': '1', 'title': 'Hello, API Design'}

large_query = execute_query(["id", "title", "body", "views"])  # => a client that needs everything
# => large_query has all 4 keys -- the SAME executor, driven purely by the requested_fields argument
print(f"large query: {large_query}")  # => Output: all four fields, because all four were requested

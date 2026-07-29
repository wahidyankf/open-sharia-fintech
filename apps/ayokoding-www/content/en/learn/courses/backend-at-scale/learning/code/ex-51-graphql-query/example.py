# pyright: strict
"""Example 51: GraphQL -- a client selects exactly the fields it needs. (co-07)

GraphQL exposes ONE endpoint where the client's QUERY names which fields to
return, solving REST's over/under-fetching. This example resolves ONLY the
requested fields from a single record.
"""

from typing import Any  # => a GraphQL response is arbitrary nested JSON


ARTICLE: dict[str, object] = {"id": 1, "title": "Hello, GraphQL", "body": "A long article body...", "author": "ada"}  # => the full record


def resolve_article(requested_fields: list[str]) -> dict[str, Any]:  # => co-07: the query picks the fields
    selected = {field: ARTICLE[field] for field in requested_fields if field in ARTICLE}  # => co-07: ONLY requested fields
    return {"data": {"article": selected}}  # => wrapped in GraphQL's own data envelope


narrow = resolve_article(["title"])  # => co-07: ask for ONLY title
print(f"query {['title']!r}:       {narrow}")  # => Output: only the title field

two_fields = resolve_article(["id", "title"])  # => co-07: ask for two fields
print(f"query {['id', 'title']!r}: {two_fields}")  # => Output: exactly those two fields

assert narrow["data"]["article"] == {"title": "Hello, GraphQL"}  # => co-07: only the requested field returns
assert set(two_fields["data"]["article"].keys()) == {"id", "title"}  # => co-07: no body/author leaked through

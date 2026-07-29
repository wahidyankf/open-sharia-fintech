# pyright: strict
"""Example 52: REST over-fetches; GraphQL does not. (co-07)

The SAME underlying data served via a fixed-shape REST response returns
EVERY field whether the caller needs them or not (over-fetching). A GraphQL
query selecting a subset returns ONLY those fields. The field/byte counts
make the gap concrete.
"""

import json  # => stdlib: count response bytes


ARTICLE: dict[str, object] = {"id": 1, "title": "Hello, GraphQL", "body": "A long article body...", "author": "ada"}  # => the full record


def rest_response() -> dict[str, object]:  # => co-07: REST returns a FIXED shape -- every field, every time
    return ARTICLE  # => the caller gets body+author even if it only wanted the title


def graphql_response(requested: list[str]) -> dict[str, object]:  # => co-07: GraphQL returns ONLY the requested fields
    return {field: ARTICLE[field] for field in requested if field in ARTICLE}  # => caller-shaped


rest = rest_response()  # => the caller only wanted the title, but REST sent everything
gql = graphql_response(["title"])  # => co-07: GraphQL sends exactly what was asked for

rest_bytes = len(json.dumps(rest))  # => the bytes REST sent
gql_bytes = len(json.dumps(gql))  # => the bytes GraphQL sent
print(f"REST returned {len(rest)} fields / {rest_bytes} bytes: {rest}")  # => Output: 4 fields, full payload
print(f"GraphQL returned {len(gql)} fields / {gql_bytes} bytes: {gql}")  # => Output: 1 field, tiny payload
print(f"GraphQL saved {rest_bytes - gql_bytes} bytes ({(1 - gql_bytes / rest_bytes) * 100:.0f}%) for this caller")  # => Output: the over-fetch gap

assert len(rest) == 4 and len(gql) == 1  # => co-07: REST over-fetched; GraphQL did not
assert gql_bytes < rest_bytes  # => co-07: the caller-shaped query transferred strictly fewer bytes

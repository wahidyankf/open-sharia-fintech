# pyright: strict
"""Capstone Step 4: graphql_facade.py -- the same data via a GraphQL facade. (co-24, co-27)

Exposes the IDENTICAL `STORE` data `rest.py`/`limits.py` serve over REST,
now through a GraphQL-shaped query executor (Examples 57-58) -- proof the
underlying data does not change when the API STYLE wrapping it does; only
the request/response shape changes.
"""

from typing import Any  # => a GraphQL response is arbitrary nested JSON

STORE: dict[int, dict[str, object]] = {  # => co-27: the IDENTICAL data rest.py/limits.py serve over REST
    1: {"id": 1, "title": "Hello, Capstone"},  # => the same seeded article
    2: {"id": 2, "title": "Capstone Article"},  # => the same article rest.py's Step 2 created
}  # => end of STORE


def graphql_query(article_id: int, requested_fields: list[str]) -> dict[str, Any]:  # => co-24: the facade query
    full_record = STORE[article_id]  # => co-27: reads from the SAME underlying data as the REST facade
    selected = {field: full_record[field] for field in requested_fields if field in full_record}
    # => co-24: returns ONLY the fields THIS query asked for, exactly like Example 58
    return {"data": {"article": selected}}  # => co-24: wrapped in GraphQL's own data envelope


rest_equivalent = {"id": 2, "title": "Capstone Article"}  # => what GET /v1/articles/2 returns over REST

graphql_response = graphql_query(2, ["id", "title"])  # => co-27: the SAME article, requested via GraphQL
print(f"GraphQL facade: {graphql_response}")  # => Output: {'data': {'article': {'id': 2, 'title': ...}}}

data_matches = graphql_response["data"]["article"] == rest_equivalent  # => co-27: equivalent data, both styles
print(f"REST and GraphQL facade return equivalent data: {data_matches}")  # => Output: True

narrow_response = graphql_query(2, ["title"])  # => co-27: GraphQL can ALSO ask for less than REST returns
print(f"GraphQL facade, title only: {narrow_response}")  # => Output: {'data': {'article': {'title': ...}}}

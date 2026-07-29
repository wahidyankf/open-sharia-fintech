# pyright: strict
"""Example 59: The Same Data via REST vs GraphQL. (co-24)

A REST endpoint (Example 1) returns its ONE fixed shape regardless of what
the caller actually needs; the SAME underlying data via GraphQL (Example
58) returns only the requested fields -- this example puts both side by
side against the identical record.
"""

RECORD = {"id": "1", "title": "Hello, API Design", "body": "A very long body...", "views": 42}
# => co-24: the single underlying record both styles serve


def rest_get_article() -> dict[str, object]:  # => co-24: REST's own fixed response shape
    return dict(RECORD)  # => co-24: ALWAYS all four fields -- the caller has no say in the shape


def graphql_query(requested_fields: list[str]) -> dict[str, object]:  # => co-24: GraphQL's selective shape
    return {field: RECORD[field] for field in requested_fields if field in RECORD}  # => only what was asked


client_needs = ["id", "title"]  # => this specific client only ever reads two fields

rest_response = rest_get_article()  # => co-24: REST call -- ignores what the client actually needs
print(f"REST returns {len(rest_response)} fields: {sorted(rest_response.keys())}")  # => Output: all 4

graphql_response = graphql_query(client_needs)  # => co-24: GraphQL call -- matches the client's own need
print(f"GraphQL returns {len(graphql_response)} fields: {sorted(graphql_response.keys())}")  # => Output: 2

wasted_fields = set(rest_response.keys()) - set(graphql_response.keys())  # => co-24: over-fetched fields
# => wasted_fields is {'body', 'views'} -- bytes this specific client paid for but never reads
print(f"REST over-fetched: {sorted(wasted_fields)}")  # => Output: ['body', 'views'] -- unused by this client

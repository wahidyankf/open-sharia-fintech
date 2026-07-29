# pyright: strict
"""Example 68: How Each Style Evolves a Field. (co-27)

Adding a field is safe in all three styles (REST's Example 32, GraphQL's
schema, gRPC's numbered proto fields), but each has its OWN specific rule
for what makes that addition safe -- this example states each rule and
demonstrates it holding.
"""

REST_V1: dict[str, object] = {"id": 1, "title": "Hello"}  # => co-27: REST -- adding a field is safe if OPTIONAL
REST_V2: dict[str, object] = {"id": 1, "title": "Hello", "author": "Ada"}  # => co-27: Example 32's own rule


def rest_old_client_reads(response: dict[str, object]) -> dict[str, object]:  # => co-27: reads known fields only
    return {"id": response["id"], "title": response["title"]}  # => ignores "author" entirely, safely


rest_before = rest_old_client_reads(REST_V1)  # => an old client against the old shape
rest_after = rest_old_client_reads(REST_V2)  # => the SAME old client against the evolved shape
print(f"REST: old client unaffected = {rest_before == rest_after}")  # => Output: True -- co-27's own claim


GRAPHQL_SCHEMA_V1_FIELDS = {"id", "title"}  # => co-27: GraphQL -- adding a NULLABLE field is safe
GRAPHQL_SCHEMA_V2_FIELDS = {"id", "title", "author"}  # => co-27: a new, optional field added to the schema


def graphql_query_still_valid(query_fields: set[str], schema_fields: set[str]) -> bool:  # => co-27: validity check
    return query_fields.issubset(schema_fields)  # => co-27: a query is valid if every field it asks for exists


old_query = {"id", "title"}  # => an existing client's own query, unaware "author" now exists
still_valid = graphql_query_still_valid(old_query, GRAPHQL_SCHEMA_V2_FIELDS)  # => co-27: checked against V2
print(f"GraphQL: old query still valid = {still_valid}")  # => Output: True -- co-27: adding "author" broke nothing


GRPC_FIELDS_V1 = {1: "id", 2: "title"}  # => co-27: gRPC -- fields are identified by NUMBER, not position
GRPC_FIELDS_V2 = {1: "id", 2: "title", 3: "author"}  # => co-27: a NEW field number, never reused


def grpc_decode_known_fields(wire_fields: dict[int, object], known: dict[int, str]) -> dict[str, object]:
    # => co-27: decodes only field numbers the OLD client's own generated code recognizes
    return {known[num]: value for num, value in wire_fields.items() if num in known}  # => unknown numbers skipped


wire_message: dict[int, object] = {1: "1", 2: "Hello", 3: "Ada"}  # => co-27: a client message, V2's schema
decoded_by_old_client = grpc_decode_known_fields(wire_message, GRPC_FIELDS_V1)  # => co-27: decoded with OLD field map
# => decoded_by_old_client has 2 keys, not 3 -- field number 3 was never even in the OLD client's map
print(f"gRPC: old client decodes = {decoded_by_old_client}")  # => Output: field 3 silently ignored, no error

# pyright: strict
"""Example 16: A Reusable Component Schema via $ref. (co-09)

Rather than repeating an `Article` shape inline at every path that needs it,
OpenAPI 3.1 declares it ONCE under `components/schemas` and every operation
references it with a `$ref` pointer string. This example resolves that
pointer by hand, the same walk a real tool performs.
"""

from typing import Any  # => the spec is arbitrary nested JSON

ARTICLE_SCHEMA = {  # => co-09: the ONE definition every $ref below points back to
    "type": "object",  # => a JSON object, not a scalar or array
    "properties": {"id": {"type": "integer"}, "title": {"type": "string"}},  # => its fields
    "required": ["id", "title"],  # => both fields are mandatory on every instance
}  # => end of ARTICLE_SCHEMA

RESPONSE_CONTENT = {"application/json": {"schema": {"$ref": "#/components/schemas/Article"}}}
# => co-09: a POINTER, not a copy -- one definition, many uses

SPEC: dict[str, Any] = {  # => co-09: components.schemas is the single source of truth
    "components": {"schemas": {"Article": ARTICLE_SCHEMA}},  # => the reusable fragment, registered once
    "paths": {  # => the operations that USE the schema above, by reference only
        "/articles/{id}": {"get": {"responses": {"200": {"content": RESPONSE_CONTENT}}}}
    },
}  # => end of SPEC


def resolve_ref(spec: dict[str, Any], ref: str) -> dict[str, Any]:  # => co-09: walks a $ref pointer
    assert ref.startswith("#/"), "only local document pointers are handled here"  # => scope guard
    path_segments = ref.removeprefix("#/").split("/")  # => e.g. ["components", "schemas", "Article"]
    node: dict[str, Any] = spec  # => start at the document root
    for segment in path_segments:  # => walk one key at a time, exactly as the pointer describes
        node = node[segment]  # => co-09: descend one level per path segment
    return node  # => the schema the $ref actually points AT


operation_response = SPEC["paths"]["/articles/{id}"]["get"]["responses"]["200"]  # => one op's response
ref_string = operation_response["content"]["application/json"]["schema"]["$ref"]  # => the pointer itself
# => ref_string is "#/components/schemas/Article" (type: str)
resolved = resolve_ref(SPEC, ref_string)  # => co-09: follow it back to components.schemas.Article
# => resolved is ARTICLE_SCHEMA itself -- the SAME object the pointer names, not a copy
print(f"$ref = {ref_string!r}")  # => Output: the raw pointer string
print(f"resolved schema: {resolved}")  # => Output: the Article schema, reached via the pointer

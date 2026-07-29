# pyright: strict
"""Example 19: Validating a Request Body Against the Schema. (co-12)

The OpenAPI schema is not just documentation -- it can gate real traffic.
This example validates an incoming request body against the `Article`
schema BEFORE the handler runs, rejecting a body that violates it.
"""

from typing import Any  # => a schema and a body are both arbitrary nested JSON

ARTICLE_SCHEMA: dict[str, Any] = {  # => co-12: the same shape Example 16 registered as a component
    "type": "object",  # => the top-level instance shape
    "properties": {"id": {"type": "integer"}, "title": {"type": "string"}},  # => the two fields
    "required": ["id", "title"],  # => both fields are mandatory
}  # => end of ARTICLE_SCHEMA


def validate_request_body(body: dict[str, Any], schema: dict[str, Any]) -> list[str]:  # => co-12 gate
    # => co-12: checked at the REQUEST boundary, before any handler logic sees the body
    errors: list[str] = []  # => accumulates every violation found
    for name in schema["required"]:  # => every required field must be present in the request
        if name not in body:  # => a required field genuinely missing from this body
            errors.append(f"missing required field {name!r}")  # => records the violation
    for name, sub in schema["properties"].items():  # => type-check every declared field present
        if name in body and sub["type"] == "integer" and not isinstance(body[name], int):  # => type check
            errors.append(f"field {name!r} must be an integer, got {type(body[name]).__name__}")  # => hit
            # => records a type mismatch against the declared schema
    return errors  # => the full, accumulated list of every violation found


good_body: dict[str, Any] = {"id": 1, "title": "Hello"}  # => matches the schema exactly
bad_body: dict[str, Any] = {"title": "Missing id"}  # => the REQUIRED "id" field is absent

print(f"good body errors: {validate_request_body(good_body, ARTICLE_SCHEMA)}")  # => Output: []
print(f"bad body errors: {validate_request_body(bad_body, ARTICLE_SCHEMA)}")  # => Output: id missing
# => bad body's error list has exactly 1 entry: "missing required field 'id'"

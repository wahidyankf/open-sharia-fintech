# pyright: strict
"""Example 20: Validating a Live Response Against the Spec. (co-12)

The same schema that gates a request can gate the RESPONSE too -- a server
that silently drifts from its own contract (an undocumented extra field, a
wrong type) is caught the moment its own response fails its own spec.
"""

from typing import Any  # => a schema and a body are both arbitrary nested JSON

ARTICLE_SCHEMA: dict[str, Any] = {  # => co-12: the contract the response is checked against
    "type": "object",  # => the top-level instance shape
    "properties": {"id": {"type": "integer"}, "title": {"type": "string"}},  # => the two fields
    "required": ["id", "title"],  # => both fields are mandatory
}  # => end of ARTICLE_SCHEMA


def validate_response_body(body: dict[str, Any], schema: dict[str, Any]) -> list[str]:  # => co-12 gate
    # => co-12: identical checking LOGIC as Example 19 -- only which side it gates differs
    errors: list[str] = []  # => accumulates every violation found
    for name in schema["required"]:  # => every required field must actually appear
        if name not in body:  # => a required field genuinely missing from this response
            errors.append(f"response is missing required field {name!r}")  # => records it
    for name, sub in schema["properties"].items():  # => type-check every declared field present
        if name in body and sub["type"] == "integer" and not isinstance(body[name], int):  # => type check
            errors.append(f"field {name!r} must be an integer, got {type(body[name]).__name__}")  # => hit
            # => records a type mismatch -- the response DRIFTED from its own declared contract
    return errors  # => the full, accumulated list of every violation found


conformant_response: dict[str, Any] = {"id": 1, "title": "Hello"}  # => matches the spec exactly
drifted_response: dict[str, Any] = {"id": "1", "title": "Hello"}  # => id has DRIFTED to a string

conformant_result = validate_response_body(conformant_response, ARTICLE_SCHEMA)  # => runs the check
# => conformant_result is [] (type: list[str]) -- no drift detected
print(f"conformant response errors: {conformant_result}")  # => Output: []

drifted_result = validate_response_body(drifted_response, ARTICLE_SCHEMA)  # => runs the check
print(f"drifted response errors: {drifted_result}")  # => Output: one error -- co-12: drift caught

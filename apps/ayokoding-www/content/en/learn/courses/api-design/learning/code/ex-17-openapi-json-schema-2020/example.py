# pyright: strict
"""Example 17: OpenAPI 3.1 Schemas Are JSON Schema Draft 2020-12. (co-10)

OpenAPI 3.1 aligns its schema object with JSON Schema Draft 2020-12
verbatim -- `type`, `minimum`, and `enum` behave exactly as JSON Schema
defines them, not an OpenAPI-specific dialect. This example applies three
2020-12 keywords with a small hand-rolled checker (no external validator
package, kept fully self-contained).
"""

from typing import Any  # => a schema is arbitrary nested JSON

ARTICLE_SCHEMA: dict[str, Any] = {  # => co-10: real JSON Schema 2020-12 keywords, unmodified
    "type": "object",  # => the top-level instance shape
    "properties": {  # => per-field constraints
        "id": {"type": "integer", "minimum": 1},  # => "minimum" is a 2020-12 keyword, used as-is
        "status": {"type": "string", "enum": ["draft", "published"]},  # => "enum" likewise
    },  # => end of the properties block
    "required": ["id", "status"],  # => both fields must be present on every instance
}  # => end of ARTICLE_SCHEMA


def check_against_schema(instance: dict[str, Any], schema: dict[str, Any]) -> list[str]:  # => co-10 checker
    # => co-10: a MINIMAL checker -- just enough of type/minimum/enum/required to demonstrate
    errors: list[str] = []  # => collects every violated keyword, not just the first
    for name in schema.get("required", []):  # => "required": every listed key MUST be present
        if name not in instance:  # => a required key genuinely missing
            errors.append(f"missing required property {name!r}")  # => records the violation
    for name, sub_schema in schema.get("properties", {}).items():  # => check each declared property
        if name not in instance:  # => nothing to check if the field itself is absent
            continue  # => already reported above by the required-keys loop if it matters
        value = instance[name]  # => the actual value supplied for this field
        if sub_schema.get("type") == "integer" and "minimum" in sub_schema:  # => a numeric floor applies
            if value < sub_schema["minimum"]:  # => "minimum": a 2020-12 numeric constraint
                errors.append(f"{name}={value} is below minimum {sub_schema['minimum']}")  # => violation
        if "enum" in sub_schema and value not in sub_schema["enum"]:  # => "enum": a closed value set
            errors.append(f"{name}={value!r} not in enum {sub_schema['enum']}")  # => violation
    return errors  # => the full, accumulated list of every keyword violated


good = {"id": 7, "status": "draft"}  # => satisfies minimum AND enum
bad = {"id": 0, "status": "archived"}  # => violates BOTH minimum (id < 1) and enum (unlisted status)

print(f"good instance errors: {check_against_schema(good, ARTICLE_SCHEMA)}")  # => Output: []
print(f"bad instance errors: {check_against_schema(bad, ARTICLE_SCHEMA)}")  # => Output: two errors
# => two errors: "id=0 is below minimum 1" and "status='archived' not in enum [...]"

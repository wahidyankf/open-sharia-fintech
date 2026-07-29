# pyright: strict
"""Example 15: A Minimal OpenAPI 3.1 Document. (co-09)

An OpenAPI document is the machine-readable contract: `openapi` (the spec
version), `info` (title/version metadata), and `paths` (the operations) are
its three required top-level keys. This example builds the smallest valid
skeleton and checks it against that requirement in code.
"""

from typing import Any  # => the spec is arbitrary nested JSON -- Any is the honest type here

GET_ARTICLE_OP = {  # => co-09: one operation object -- kept as its own value, flat and readable
    "summary": "Get an article by id",  # => a human-readable one-liner
    "responses": {"200": {"description": "OK"}},  # => the happy-path response
}  # => end of GET_ARTICLE_OP

OPENAPI_SPEC: dict[str, Any] = {  # => co-09: a Python dict standing in for the YAML/JSON doc
    "openapi": "3.1.0",  # => co-09: pins the spec VERSION this document conforms to
    "info": {"title": "Articles API", "version": "1.0.0"},  # => required metadata block
    "paths": {"/articles/{id}": {"get": GET_ARTICLE_OP}},  # => co-09: every operation lives under paths
}  # => end of OPENAPI_SPEC
# => OPENAPI_SPEC has exactly 3 top-level keys: "openapi", "info", "paths"


def validate_skeleton(spec: dict[str, Any]) -> list[str]:  # => co-09: the three-key floor check
    required_keys = ("openapi", "info", "paths")  # => the minimum a document MUST declare
    missing = [key for key in required_keys if key not in spec]  # => anything absent is a failure
    return missing  # => an empty list means the skeleton is valid


missing_keys = validate_skeleton(OPENAPI_SPEC)  # => run the check against the document above
# => missing_keys is [] (type: list[str]) -- all three required keys are present
print(f"missing required keys: {missing_keys}")  # => Output: [] -- all three keys present
print(f"declared paths: {list(OPENAPI_SPEC['paths'].keys())}")  # => Output: ['/articles/{id}']

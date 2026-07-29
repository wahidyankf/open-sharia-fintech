# pyright: strict
"""Example 49: Declaring bearer/apiKey Security Schemes in OpenAPI. (co-34)

Auth (Examples 46-48) belongs in the CONTRACT, not just the handler code --
OpenAPI's `securitySchemes` declares each scheme ONCE, and an operation's
own `security` field states which scheme(s) it requires.
"""

from typing import Any  # => the spec is arbitrary nested JSON

BEARER_SCHEME = {"type": "http", "scheme": "bearer"}  # => co-34: matches Example 46's RFC 6750 syntax
API_KEY_SCHEME = {"type": "apiKey", "in": "header", "name": "X-API-Key"}  # => co-34: matches Example 47

SECURITY_SCHEMES = {"bearerAuth": BEARER_SCHEME, "apiKeyAuth": API_KEY_SCHEME}  # => co-34: registered by name
DELETE_OPERATION = {"security": [{"bearerAuth": ["articles:write"]}]}  # => co-34: scheme name + required scope

SPEC: dict[str, Any] = {  # => co-34: security schemes declared under components, referenced by name
    "components": {"securitySchemes": SECURITY_SCHEMES},  # => the ONE place every scheme is defined
    "paths": {"/articles/{id}": {"delete": DELETE_OPERATION}},  # => the operation that USES one scheme
}  # => end of SPEC


def declared_schemes(spec: dict[str, Any]) -> list[str]:  # => co-34: every scheme name the spec registers
    return list(spec["components"]["securitySchemes"].keys())  # => the two names declared above


def operation_requirement(spec: dict[str, Any]) -> dict[str, list[str]]:  # => co-34: what ONE op requires
    delete_op = spec["paths"]["/articles/{id}"]["delete"]  # => the specific operation to inspect
    return delete_op["security"][0]  # => co-34: the first (and here, only) security requirement


print(f"declared schemes: {declared_schemes(SPEC)}")  # => Output: ['bearerAuth', 'apiKeyAuth']
print(f"DELETE requires: {operation_requirement(SPEC)}")  # => Output: {'bearerAuth': ['articles:write']}
# => a client (or a codegen tool) can now discover the auth requirement WITHOUT reading handler code

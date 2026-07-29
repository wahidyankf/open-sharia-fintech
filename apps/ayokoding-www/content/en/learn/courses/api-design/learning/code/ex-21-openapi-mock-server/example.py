# pyright: strict
"""Example 21: Serving a Mock from the Spec's Own Examples. (co-11)

A mock server needs no business logic at all -- it reads the `example`
value the spec ALREADY declares for a response and serves that verbatim.
This is what lets a frontend team start building against an API before its
real handlers exist.
"""

from typing import Any  # => the spec is arbitrary nested JSON

SPEC_EXAMPLE = {"id": 1, "title": "Hello, API Design"}  # => co-11: the spec-declared example itself
# => SPEC_EXAMPLE is {'id': 1, 'title': 'Hello, API Design'} (type: dict[str, object])

RESPONSE_CONTENT = {"application/json": {"example": SPEC_EXAMPLE}}  # => the example lives under content

SPEC: dict[str, Any] = {  # => co-11: the example lives INSIDE the spec, not in separate test fixtures
    "paths": {"/articles/{id}": {"get": {"responses": {"200": {"content": RESPONSE_CONTENT}}}}}
}  # => end of SPEC


def mock_response(spec: dict[str, Any], path: str, method: str, status: str) -> dict[str, Any]:
    # => co-11: a mock server literally IS this one dict lookup -- no handler code required
    operation_responses = spec["paths"][path][method]["responses"][status]  # => this op's own response
    return operation_responses["content"]["application/json"]["example"]  # => co-11: serves it verbatim


mocked = mock_response(SPEC, "/articles/{id}", "get", "200")  # => "call" the mock endpoint
# => mocked is the SAME dict object as SPEC_EXAMPLE, reached purely by walking the spec
print(f"mocked response: {mocked}")  # => Output: {'id': 1, 'title': 'Hello, API Design'}
assert mocked == SPEC_EXAMPLE  # => co-11: proves the mock served the spec's example VERBATIM, not a copy

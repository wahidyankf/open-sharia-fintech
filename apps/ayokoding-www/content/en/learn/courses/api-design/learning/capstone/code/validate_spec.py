# pyright: strict
"""Capstone Step 1: validate_spec.py -- the spec validates, and a mock server serves it. (co-09, co-14)

Re-encodes `../openapi.yaml`'s structure as a Python dict (the same pattern
Examples 70-72 use for their own OpenAPI specs), asserts the required fields
this capstone's REST/idempotency/rate-limit steps depend on, and builds a
tiny mock server that returns a canned response conforming to each declared
schema -- proof the CONTRACT alone is enough to know what a real handler
must return, before Step 2 writes one.
"""

from typing import Any  # => the spec is arbitrary nested JSON, mirroring openapi.yaml

SPEC: dict[str, Any] = {  # => co-09: the SAME structure openapi.yaml declares, as a Python dict
    "openapi": "3.1.0",  # => co-09: matches openapi.yaml's own version declaration
    "paths": {  # => co-09: every operation the mock server below must be able to answer
        "/v1/articles": {  # => the collection resource
            "get": {"required_response_fields": ["edges", "pageInfo"]},  # => co-17: the connection envelope
            "post": {"required_response_fields": ["id", "title"]},  # => co-18: the created (or replayed) article
        },  # => end of /v1/articles
        "/v1/articles/{id}": {  # => the item resource
            "get": {"required_response_fields": ["id", "title"]},  # => the found article's own shape
        },  # => end of /v1/articles/{id}
    },  # => end of paths
}  # => end of SPEC


def spec_validates(spec: dict[str, Any]) -> bool:  # => co-09: a minimal structural validity check
    has_version = spec.get("openapi", "").startswith("3.1")  # => co-09: this course targets OpenAPI 3.1
    has_paths = len(spec.get("paths", {})) > 0  # => co-09: a spec with zero paths documents nothing
    return has_version and has_paths  # => both must hold for this spec to count as "validates"


def mock_response_for(spec: dict[str, Any], path: str, method: str) -> dict[str, object]:  # => co-09: mock server
    required = spec["paths"][path][method]["required_response_fields"]  # => co-09: what THIS op must return
    canned: dict[str, object] = {  # => co-09: one hand-built canned value per possible field
        "id": 1,  # => a plausible integer id
        "title": "Hello, Capstone",  # => a plausible title
        "edges": [{"node": {"id": 1, "title": "Hello, Capstone"}, "cursor": "1"}],  # => one edge
        "pageInfo": {"hasNextPage": False, "endCursor": "1"},  # => a terminal page
    }  # => end of canned
    return {field: canned[field] for field in required}  # => co-09: only the fields THIS operation promises


valid = spec_validates(SPEC)  # => co-09: checks the spec itself, before serving anything from it
print(f"spec validates: {valid}")  # => Output: True

list_response = mock_response_for(SPEC, "/v1/articles", "get")  # => mocks GET /v1/articles
print(f"mock GET /v1/articles: {list_response}")  # => Output: an edges/pageInfo envelope

create_response = mock_response_for(SPEC, "/v1/articles", "post")  # => mocks POST /v1/articles
print(f"mock POST /v1/articles: {create_response}")  # => Output: id + title

item_response = mock_response_for(SPEC, "/v1/articles/{id}", "get")  # => mocks GET /v1/articles/{id}
print(f"mock GET /v1/articles/{{id}}: {item_response}")  # => Output: id + title

for path, methods in SPEC["paths"].items():  # => co-09: verifies EVERY declared operation, not just three
    for method, operation in methods.items():  # => walks every method under this path
        response = mock_response_for(SPEC, path, method)  # => builds the mock response for this operation
        assert set(response.keys()) == set(operation["required_response_fields"])  # => co-09: exact match
print("mock server serves every declared operation, matching its exact required fields")  # => Output

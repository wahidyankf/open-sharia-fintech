# pyright: strict
"""Example 79: Generating Human Docs (Swagger UI / Redoc) From the Spec. (co-11)

Human-readable API documentation (Swagger UI, Redoc) is GENERATED from the
same OpenAPI spec that already drives validation (Example 12) and mocking
-- ONE source of truth, never a hand-written doc page that silently drifts
from what the API actually does.
"""

from typing import Any  # => the spec is arbitrary nested JSON

SPEC: dict[str, Any] = {  # => co-11: the SAME kind of spec Examples 12 and 70-72 already use
    "info": {"title": "Articles API", "version": "1.0.0"},  # => co-11: metadata every doc page needs
    "paths": {  # => co-11: every operation the generated docs will list
        "/articles/{id}": {  # => co-11: one path, with two documented operations
            "get": {"summary": "Fetch a single article by id"},  # => co-11: a human-readable summary
            "put": {"summary": "Replace an article's title (idempotent)"},  # => Example 4's own semantics
        },  # => end of /articles/{id}
        "/articles": {  # => co-11: a second path, with one documented operation
            "post": {"summary": "Create a new article"},  # => Example 5's own semantics
        },  # => end of /articles
    },  # => end of paths
}  # => end of SPEC


def generate_docs_page(spec: dict[str, Any]) -> str:  # => co-11: the "Swagger UI / Redoc" generation step
    lines = [f"# {spec['info']['title']} (v{spec['info']['version']})", ""]  # => co-11: a title line, from the spec
    for path, operations in spec["paths"].items():  # => co-11: one section per PATH
        for method, operation in operations.items():  # => co-11: one line per OPERATION on that path
            lines.append(f"- {method.upper()} {path} -- {operation['summary']}")  # => co-11: generated, not hand-typed
    return "\n".join(lines)  # => co-11: the FULL generated documentation page


docs_page = generate_docs_page(SPEC)  # => co-11: runs the generator against the live spec
print(docs_page)  # => Output: a title line plus one bullet per operation, all pulled from SPEC

operation_count = sum(len(ops) for ops in SPEC["paths"].values())  # => co-11: counts every documented operation
# => operation_count is 3 (type: int) -- if SPEC gains a 4th operation, the docs regenerate automatically
print(f"\ndocumented {operation_count} operations")  # => Output: 3 -- GET, PUT, and POST, all rendered

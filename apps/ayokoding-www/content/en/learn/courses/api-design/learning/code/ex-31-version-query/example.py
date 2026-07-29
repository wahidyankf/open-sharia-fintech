# pyright: strict
"""Example 31: Versioning via a Query Parameter. (co-13)

Azure's guideline uses `?api-version=YYYY-MM-DD`, and treats a MISSING
parameter as an error (`400 MissingApiVersionParameter`) rather than a
silent default -- forcing every caller to be explicit about its version.
"""

from dataclasses import dataclass  # => a small typed response record for this example


@dataclass  # => co-13: status plus a small JSON-shaped body
class Response:
    status: int  # => the HTTP status code
    body: dict[str, object]  # => either the resolved data or an error description


def get_article(api_version: str | None) -> Response:  # => GET /articles/1?api-version=
    if api_version is None:  # => co-13: Azure's own rule -- missing means reject, not default
        return Response(400, {"error": "MissingApiVersionParameter"})  # => 400, explicit rejection
    return Response(200, {"id": 1, "title": "Hello", "api_version": api_version})  # => echoes the version


missing = get_article(api_version=None)  # => request 1: no ?api-version= at all
# => missing.status is 400 -- Azure's rule rejects silence, unlike most other version strategies
print(f"missing: status={missing.status}, body={missing.body}")  # => Output: 400, MissingApiVersionParameter

present = get_article(api_version="2026-01-01")  # => request 2: explicit version given
print(f"present: status={present.status}, body={present.body}")  # => Output: 200, echoes the version

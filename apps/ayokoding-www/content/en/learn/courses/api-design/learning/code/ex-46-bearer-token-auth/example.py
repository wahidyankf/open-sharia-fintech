# pyright: strict
"""Example 46: Authorization: Bearer <token>. (co-23)

RFC 6750 defines the `Authorization: Bearer <token>` syntax carrying an
OAuth 2.0 (RFC 6749) access token -- a request with NO token is rejected
with `401 Unauthorized`, distinct from Example 48's scope-based `403`.
"""

from dataclasses import dataclass  # => a small typed response record for this example

VALID_TOKENS: set[str] = {"token-abc-123"}  # => co-23: the set of currently-valid bearer tokens


@dataclass  # => co-23: status plus a small body describing the outcome
class Response:
    status: int  # => the HTTP status code
    body: dict[str, str]  # => the resource, or an authentication error description


def get_article(authorization_header: str | None) -> Response:  # => GET /articles/1, auth-gated
    if authorization_header is None:  # => co-23: NO Authorization header at all
        return Response(401, {"error": "missing Authorization header"})  # => 401, rejected outright
    if not authorization_header.startswith("Bearer "):  # => co-23: the WRONG scheme (not "Bearer")
        return Response(401, {"error": "expected a Bearer token"})  # => 401, malformed scheme
    token = authorization_header.removeprefix("Bearer ")  # => co-23: RFC 6750's exact syntax, unpacked
    if token not in VALID_TOKENS:  # => co-23: a syntactically valid but UNKNOWN token
        return Response(401, {"error": "invalid token"})  # => 401, still an authentication failure
    return Response(200, {"id": "1", "title": "Hello"})  # => 200, a genuinely valid bearer token


missing = get_article(authorization_header=None)  # => request 1: no header at all
print(f"missing: status={missing.status}, body={missing.body}")  # => Output: 401

valid = get_article(authorization_header="Bearer token-abc-123")  # => request 2: RFC 6750 syntax, valid token
# => all three rejection paths return 401 -- co-23 never leaks WHICH check failed to the caller
print(f"valid: status={valid.status}, body={valid.body}")  # => Output: 200

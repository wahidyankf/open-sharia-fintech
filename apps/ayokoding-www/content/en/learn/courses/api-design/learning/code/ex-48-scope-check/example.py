# pyright: strict
"""Example 48: Scope-Gated Authorization. (co-23)

OAuth scopes are space-delimited, case-sensitive strings (RFC 6749). A
token can be VALID (Example 46) but still lack the SPECIFIC scope an
operation requires -- that gap is `403 Forbidden`, not `401 Unauthorized`.
"""

from dataclasses import dataclass  # => a small typed response record for this example

TOKEN_SCOPES: dict[str, set[str]] = {  # => co-23: token -> the space-delimited scopes it actually carries
    "token-reader": {"articles:read"},  # => can read, but nothing else
    "token-writer": {"articles:read", "articles:write"},  # => can read AND write
}  # => end of TOKEN_SCOPES


@dataclass  # => co-23: status plus a small body describing the outcome
class Response:
    status: int  # => the HTTP status code
    body: dict[str, str]  # => the resource, or an authorization error description


def delete_article(token: str, required_scope: str) -> Response:  # => DELETE /articles/1, scope-gated
    scopes = TOKEN_SCOPES.get(token, set())  # => co-23: the token's OWN granted scopes, if any
    if required_scope not in scopes:  # => co-23: a VALID token, but missing the SPECIFIC scope needed
        return Response(403, {"error": f"missing required scope {required_scope!r}"})  # => 403, forbidden
    return Response(204, {})  # => 204 -- the scope check passed, the delete succeeded (co-07's shape)


out_of_scope = delete_article("token-reader", required_scope="articles:write")  # => a reader, needs write
# => 403, not 401 -- the token itself is perfectly valid, it just lacks this one scope
print(f"out of scope: status={out_of_scope.status}, body={out_of_scope.body}")  # => Output: 403

in_scope = delete_article("token-writer", required_scope="articles:write")  # => a writer, needs write
print(f"in scope: status={in_scope.status}, body={in_scope.body}")  # => Output: 204

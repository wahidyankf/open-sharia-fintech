# pyright: strict
"""Example 47: The X-API-Key Header. (co-23)

An API key is a simpler alternative to OAuth's bearer token -- a single,
long-lived secret carried in a custom header (`X-API-Key`), checked against
a known set; an INVALID key is rejected the same way Example 46's does.
"""

from dataclasses import dataclass  # => a small typed response record for this example

VALID_API_KEYS: set[str] = {"key-live-abcdef"}  # => co-23: the set of currently-valid API keys


@dataclass  # => co-23: status plus a small body describing the outcome
class Response:
    status: int  # => the HTTP status code
    body: dict[str, str]  # => the resource, or an authentication error description


def get_article(x_api_key: str | None) -> Response:  # => GET /articles/1, API-key-gated
    if x_api_key is None:  # => co-23: no X-API-Key header at all
        return Response(401, {"error": "missing X-API-Key header"})  # => 401, rejected outright
    if x_api_key not in VALID_API_KEYS:  # => co-23: a KEY was supplied, but it is not a KNOWN one
        return Response(401, {"error": "invalid API key"})  # => 401, an invalid credential
    return Response(200, {"id": "1", "title": "Hello"})  # => 200, a genuinely valid key


invalid = get_article(x_api_key="key-wrong-999999")  # => request 1: a key, but the WRONG one
print(f"invalid: status={invalid.status}, body={invalid.body}")  # => Output: 401

valid = get_article(x_api_key="key-live-abcdef")  # => request 2: the correct, known key
# => an API key is simpler than a bearer token to check, but it never expires on its own
print(f"valid: status={valid.status}, body={valid.body}")  # => Output: 200

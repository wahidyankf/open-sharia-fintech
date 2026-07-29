# pyright: strict
"""Example 43: ETag + If-None-Match -> 304 Not Modified. (co-22)

The server computes an `ETag` (a content hash); a client resending it via
`If-None-Match` gets `304 Not Modified` with an EMPTY body when the content
has not changed -- saving the bandwidth of re-sending unchanged data.
"""

import hashlib  # => stdlib: computes the ETag as a content hash
from dataclasses import dataclass  # => a small typed response record for this example

ARTICLE_BODY = '{"id": 1, "title": "Hello"}'  # => the resource's current serialized content


def compute_etag(body: str) -> str:  # => co-22: a deterministic hash of the CURRENT content
    return hashlib.sha256(body.encode()).hexdigest()[:12]  # => a short, stable content fingerprint


@dataclass  # => co-22: status, headers (the ETag), and a body that may be empty on a 304
class Response:
    status: int  # => the HTTP status code
    headers: dict[str, str]  # => carries the ETag
    body: str  # => empty on a 304, populated on a 200


def get_article(if_none_match: str | None) -> Response:  # => GET /articles/1, conditional-aware
    current_etag = compute_etag(ARTICLE_BODY)  # => co-22: recomputed fresh on every call
    if if_none_match == current_etag:  # => co-22: the client's cached copy is STILL valid
        return Response(304, {"ETag": current_etag}, "")  # => 304 -- no need to resend the body
    return Response(200, {"ETag": current_etag}, ARTICLE_BODY)  # => 200 -- full body, plus the ETag


first = get_article(if_none_match=None)  # => request 1: no cached copy yet
print(f"first: status={first.status}, body={first.body!r}")  # => Output: 200, full body

cached_etag = first.headers["ETag"]  # => the client REMEMBERS this ETag for next time
second = get_article(if_none_match=cached_etag)  # => request 2: resends the SAME ETag
# => second.body is "" -- the server saved the bandwidth of resending unchanged content
print(f"second: status={second.status}, body={second.body!r}")  # => Output: 304, empty body -- unchanged

# pyright: strict
"""Example 45: Optimistic Concurrency with If-Match. (co-22)

`If-Match` requires a PUT's supplied ETag to match the CURRENT one before
the write is allowed -- a stale write (one based on outdated data) is
rejected with `412 Precondition Failed` instead of silently overwriting.
"""

from dataclasses import dataclass  # => a small typed response record for this example

ARTICLE = {"title": "Original title", "etag": "v1-abc123"}  # => co-22: the resource carries its own ETag


@dataclass  # => co-22: status plus a small body describing the outcome
class Response:
    status: int  # => the HTTP status code
    body: dict[str, str]  # => the updated resource, or an error description


def put_article(new_title: str, if_match: str) -> Response:  # => PUT /articles/1, optimistic-concurrency-aware
    if if_match != ARTICLE["etag"]:  # => co-22: the caller's ETag does NOT match the CURRENT one
        return Response(412, {"error": "Precondition Failed: resource has changed"})  # => 412, rejected
    ARTICLE["title"] = new_title  # => co-22: the write is only applied AFTER the ETag check passes
    ARTICLE["etag"] = "v2-def456"  # => co-22: a successful write ALSO advances the ETag
    return Response(200, {"title": ARTICLE["title"], "etag": ARTICLE["etag"]})  # => 200, the new state


stale_write = put_article("Stale update", if_match="v1-WRONG")  # => a caller with an OUTDATED etag
# => ARTICLE["title"] is still "Original title" -- the stale write never actually applied
print(f"stale write: status={stale_write.status}, body={stale_write.body}")  # => Output: 412, rejected

fresh_write = put_article("Fresh update", if_match="v1-abc123")  # => a caller with the CURRENT etag
print(f"fresh write: status={fresh_write.status}, body={fresh_write.body}")  # => Output: 200, applied

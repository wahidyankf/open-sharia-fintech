# pyright: strict
"""Example 45: ETag + If-None-Match -> 304 Not Modified. (co-24)

The server tags a representation with an opaque ETag; a client resending
If-None-Match with the SAME tag gets 304 (no body) when the representation
is unchanged. A different tag -> 200 with the full body. Source: RFC 9111
(HTTP Caching, 2022).
"""

import hashlib  # => stdlib: derive a stable ETag from the representation


STORE: dict[int, str] = {1: "Hello, world"}  # => the resource


def etag_of(text: str) -> str:  # => co-24: a stable opaque tag derived from the representation
    return '"' + hashlib.sha256(text.encode()).hexdigest()[:16] + '"'  # => a quoted short hash


def get_with_etag(item_id: int, if_none_match: str | None) -> tuple[int, dict[str, str], str]:
    # => co-24: returns (status, headers, body)
    value = STORE.get(item_id, "")  # => the current representation
    current_etag = etag_of(value)  # => the current tag
    headers = {"ETag": current_etag}  # => every response carries the current tag
    if if_none_match == current_etag:  # => co-24: the client's tag MATCHES -> nothing changed
        return 304, headers, ""  # => 304, NO body
    return 200, headers, value  # => 200, full body


# First fetch: client has no tag -> full body + the new ETag.
status, headers, body = get_with_etag(1, if_none_match=None)
print(f"first fetch: status={status}, ETag={headers['ETag']}, body={body!r}")  # => Output: 200, full body

# Revalidation: client resends the SAME tag -> 304 (no body re-sent).
client_etag = headers["ETag"]  # => the tag the client remembered
status2, headers2, body2 = get_with_etag(1, if_none_match=client_etag)
print(f"revalidate (match): status={status2}, body={body2!r}")  # => Output: 304, empty body

# A stale tag (representation changed) -> 200 with the new body.
STORE[1] = "Hello, world (edited)"  # => the resource changed
status3, headers3, body3 = get_with_etag(1, if_none_match=client_etag)  # => old tag no longer matches
print(f"after change (stale tag): status={status3}, body={body3!r}")  # => Output: 200, new body

assert status == 200 and status2 == 304  # => co-24: match -> 304, no body re-sent
assert status3 == 200 and headers3["ETag"] != client_etag  # => co-24: changed -> new tag + full body

# pyright: strict
"""Example 44: The Cache-Control: max-age Directive. (co-22)

`Cache-Control` tells the CLIENT (or an intermediary cache) how long a
response may be reused WITHOUT even asking the server -- distinct from
`ETag`'s "ask, and I'll tell you if it changed" (Example 43).
"""

from dataclasses import dataclass  # => a small typed response record for this example


@dataclass  # => co-22: status, headers (the caching directive), and the body
class Response:  # => co-22: max-age is a header, not a change to the status or body shape
    status: int  # => the HTTP status code
    headers: dict[str, str]  # => carries the Cache-Control directive
    body: dict[str, object]  # => the resource's own data


def get_article() -> Response:  # => GET /articles/1 -- a response that is safe to cache briefly
    return Response(  # => co-22: max-age=60 means "reusable for 60 seconds, no request needed"
        status=200,  # => a normal successful GET
        headers={"Cache-Control": "max-age=60"},  # => co-22: the caching directive itself
        body={"id": 1, "title": "Hello"},  # => the resource's own data
    )  # => end of the Response construction


def parse_max_age(cache_control: str) -> int:  # => co-22: a client parsing the directive's own value
    directive_value = cache_control.split("max-age=")[1]  # => extracts just the number part
    return int(directive_value)  # => co-22: how many seconds the client may reuse this response


response = get_article()  # => run the handler
print(f"Cache-Control={response.headers['Cache-Control']}")  # => Output: Cache-Control=max-age=60

max_age_seconds = parse_max_age(response.headers["Cache-Control"])  # => co-22: parses it back to an int
# => max_age_seconds is 60 (type: int) -- the client may skip a full round trip for this long
print(f"parsed max_age: {max_age_seconds} seconds")  # => Output: parsed max_age: 60 seconds

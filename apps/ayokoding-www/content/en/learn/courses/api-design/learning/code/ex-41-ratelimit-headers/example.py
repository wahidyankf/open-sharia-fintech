# pyright: strict
"""Example 41: Structured RateLimit / RateLimit-Policy Headers. (co-20)

`draft-ietf-httpapi-ratelimit-headers-11` (active, unlike Example 39's
lapsed idempotency draft) standardizes `RateLimit`/`RateLimit-Policy` --
structured fields exposing remaining quota, replacing ad-hoc `X-RateLimit-*`.
"""

from dataclasses import dataclass  # => a small typed response record for this example


@dataclass  # => co-20: status plus the structured rate-limit headers
class Response:  # => co-20: both header fields ride alongside a normal, successful status
    status: int  # => the HTTP status code
    headers: dict[str, str]  # => carries the structured RateLimit fields


def call_api(remaining: int, limit: int, window_seconds: int) -> Response:  # => one API call, quota-aware
    return Response(  # => co-20: exposes the CURRENT quota state on every call, success or not
        status=200,  # => this example models a successful call still within budget
        headers={  # => the two draft-defined structured header fields
            "RateLimit": f"limit={limit}, remaining={remaining}",  # => co-20: this call's own quota state
            "RateLimit-Policy": f"{limit};w={window_seconds}",  # => co-20: the POLICY -- limit + window
        },  # => end of the headers dict
    )  # => end of the Response construction


response = call_api(remaining=42, limit=100, window_seconds=3600)  # => a call with quota still available
print(f"status={response.status}")  # => Output: status=200
print(f"RateLimit={response.headers['RateLimit']}")  # => Output: limit=100, remaining=42
print(f"RateLimit-Policy={response.headers['RateLimit-Policy']}")  # => Output: 100;w=3600


def parse_remaining(headers: dict[str, str]) -> int:  # => co-20: a client parsing the structured field
    ratelimit_value = headers["RateLimit"]  # => the raw header string
    remaining_part = ratelimit_value.split("remaining=")[1]  # => co-20: extracts just the number
    return int(remaining_part)  # => co-20: a client can react to "how much quota is left"


parsed = parse_remaining(response.headers)  # => co-20: a client parses the header back into a number
# => parsed is 42 (type: int) -- matches what the server set exactly
print(f"parsed remaining: {parsed}")  # => Output: 42 -- matches what the server set

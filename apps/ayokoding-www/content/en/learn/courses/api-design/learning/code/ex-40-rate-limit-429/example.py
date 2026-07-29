# pyright: strict
"""Example 40: 429 Too Many Requests + Retry-After. (co-19)

RFC 6585's `429` communicates a rate limit was exceeded; an optional
`Retry-After` header tells the caller how long to wait before trying again
-- a simple fixed-budget counter is enough to demonstrate the contract.
"""

from dataclasses import dataclass, field  # => field: default_factory for the headers dict

REQUEST_BUDGET = [3]  # => a mutable counter cell -- 3 requests allowed before the limit trips


@dataclass  # => co-19: status plus headers, so Retry-After is only present when relevant
class Response:  # => co-19: an empty headers dict means "no Retry-After needed"
    status: int  # => the HTTP status code
    headers: dict[str, str] = field(default_factory=dict[str, str])  # => carries Retry-After when limited


def call_api() -> Response:  # => a single API call, gated by the shared budget above
    if REQUEST_BUDGET[0] <= 0:  # => co-19: the budget is exhausted
        return Response(status=429, headers={"Retry-After": "60"})  # => co-19: 429 + how long to wait
    REQUEST_BUDGET[0] -= 1  # => co-19: consumes one unit of budget on a successful call
    return Response(status=200)  # => a normal, successful call


results = [call_api() for _ in range(4)]  # => co-19: 4 calls against a budget of 3 -- the 4th trips it
# => results has 4 elements; the first 3 are status 200, the 4th is status 429
for i, response in enumerate(results, start=1):  # => print every call's own outcome
    has_retry = "Retry-After" in response.headers  # => True only for the 429 call
    extra = f", Retry-After={response.headers['Retry-After']}" if has_retry else ""  # => co-19: conditional
    print(f"call {i}: status={response.status}{extra}")  # => Output: 200,200,200, then 429 + Retry-After

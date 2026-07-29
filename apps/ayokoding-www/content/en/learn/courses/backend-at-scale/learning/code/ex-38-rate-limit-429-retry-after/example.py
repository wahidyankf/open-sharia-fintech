# pyright: strict
"""Example 38: 429 Too Many Requests + Retry-After. (co-20)

When a caller exceeds its rate limit, the response is 429 with a Retry-After
header telling the caller how long to wait before retrying. Source: RFC 6585
Sec 4 (429) and RFC 9110 (Retry-After semantics).
"""

from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-20: status + headers (Retry-After lives here) + body
class Response:
    status: int  # => 200 when allowed, 429 when over the limit
    headers: dict[str, str] = field(default_factory=dict[str, str])  # => carries Retry-After on a 429
    body: dict[str, str] = field(default_factory=dict[str, str])  # => a short message


BUDGET = [3]  # => a mutable budget cell: 3 calls allowed per window


def create_order() -> Response:  # => POST /orders -- rate-limited
    if BUDGET[0] <= 0:  # => co-20: over the limit -> 429
        return Response(status=429, headers={"Retry-After": "60"}, body={"error": "too many requests"})  # => 429 + hint
    BUDGET[0] -= 1  # => consume one unit of budget
    return Response(status=201, body={"status": "created"})  # => within budget -> 201


call_1 = create_order()  # => budget 3 -> 2
call_2 = create_order()  # => budget 2 -> 1
call_3 = create_order()  # => budget 1 -> 0
call_4 = create_order()  # => budget 0 -> over the limit
for i, resp in enumerate((call_1, call_2, call_3, call_4), start=1):
    retry = resp.headers.get("Retry-After", "-")  # => show Retry-After when present
    print(f"call {i}: status={resp.status}, Retry-After={retry}")  # => Output: 201,201,201,429

assert call_1.status == 201 and call_2.status == 201 and call_3.status == 201  # => the three compliant calls passed
assert call_4.status == 429 and call_4.headers["Retry-After"] == "60"  # => co-20: 429 carries a Retry-After hint

# pyright: strict
"""Example 74: Combining Idempotency + Rate Limiting on One Endpoint. (co-18, co-19)

Idempotency (Examples 37-39) and rate limiting (Examples 40-42) are
INDEPENDENT concerns that both apply to the SAME write endpoint at once --
this example checks the rate limit FIRST (a rejected call should not even
reach idempotency bookkeeping), then applies idempotency second.
"""

from dataclasses import dataclass, field  # => field: default_factory for the headers dict

REQUEST_BUDGET = [2]  # => co-19: a small budget -- 2 calls allowed before 429 trips
IDEMPOTENCY_STORE: dict[str, dict[str, object]] = {}  # => co-18: key -> the response it produced


@dataclass  # => co-18/co-19: status, headers (Retry-After when limited), and the body
class Response:
    status: int  # => the HTTP status code
    headers: dict[str, str] = field(default_factory=dict[str, str])  # => carries Retry-After when limited
    body: dict[str, object] = field(default_factory=dict[str, object])  # => the charge, when one is returned


def create_charge(idempotency_key: str, amount: int) -> Response:  # => POST /charges, both concerns combined
    if REQUEST_BUDGET[0] <= 0:  # => co-19: rate limit is checked FIRST -- before any idempotency bookkeeping
        return Response(status=429, headers={"Retry-After": "60"})  # => co-19: rejected, key never recorded
    if idempotency_key in IDEMPOTENCY_STORE:  # => co-18: a REPLAY, checked only AFTER the budget allows it
        return Response(status=200, body=IDEMPOTENCY_STORE[idempotency_key])  # => co-18: the stored response
    REQUEST_BUDGET[0] -= 1  # => co-19: consumes budget only for a genuinely NEW request
    body: dict[str, object] = {"id": 1, "amount": amount, "status": "succeeded"}  # => explicit dict[str, object]
    IDEMPOTENCY_STORE[idempotency_key] = body  # => co-18: recorded for any future replay
    return Response(status=201, body=body)  # => 201 -- a freshly created charge


first = create_charge("key-1", 5000)  # => call 1: new key, budget=2 -> 1
print(f"call 1 (new key): status={first.status}, body={first.body}")  # => Output: 201

replay = create_charge("key-1", 5000)  # => call 2: SAME key -- co-18's replay path, budget STILL 1
print(f"call 2 (replay): status={replay.status}, body={replay.body}")  # => Output: 200, IDENTICAL body

replay_again = create_charge("key-1", 5000)  # => call 3: ANOTHER replay of the SAME key
print(f"call 3 (replay): status={replay_again.status}")  # => Output: 200 -- budget untouched by replays

new_key = create_charge("key-2", 3000)  # => call 4: a genuinely NEW key -- consumes the LAST budget unit
print(f"call 4 (new key): status={new_key.status}")  # => Output: 201, budget=2 -> 1 -> 0

exhausted = create_charge("key-3", 1000)  # => call 5: yet ANOTHER new key -- budget is now exhausted
# => exhausted.status is 429 -- the two independent concerns compose: budget gates BEFORE idempotency
print(f"call 5 (new key, no budget): status={exhausted.status}")  # => Output: 429 -- co-19's own rejection

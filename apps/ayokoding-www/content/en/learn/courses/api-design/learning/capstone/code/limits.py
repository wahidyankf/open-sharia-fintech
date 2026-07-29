# pyright: strict
"""Capstone Step 3: limits.py -- add rate limiting on top of Step 2's endpoint. (co-19, co-20)

Wraps `rest.py`'s `create_article_v1` with a shared request budget -- an
over-limit caller receives `429` with the correct `Retry-After` and
structured `RateLimit` headers (Examples 40-41), while a compliant caller
still succeeds normally. Following Example 74's own ordering, the rate
limit is checked BEFORE idempotency -- a replay never consumes budget
while budget remains, but once budget is exhausted even a replay is
rejected with `429`, since it never reaches the idempotency check at all.
"""

from dataclasses import dataclass, field  # => field: default_factory for mutable dataclass defaults

STORE: dict[int, dict[str, object]] = {1: {"id": 1, "title": "Hello, Capstone"}}  # => co-09: seed data
IDEMPOTENCY_STORE: dict[str, dict[str, object]] = {}  # => co-18: key -> the response it produced
NEXT_ID = [2]  # => a mutable counter cell -- the next id after the seeded article
REQUEST_BUDGET = [3]  # => co-19: a small budget -- 3 calls allowed before 429 trips


@dataclass  # => co-19/co-20: status, headers (Retry-After + RateLimit), and the body
class Response:
    status: int  # => the HTTP status code
    headers: dict[str, str] = field(default_factory=dict[str, str])  # => carries rate-limit headers
    body: dict[str, object] = field(default_factory=dict[str, object])  # => the resource, when returned


def create_article_v1_rate_limited(idempotency_key: str, title: str) -> Response:  # => POST, rate-limit-aware
    if REQUEST_BUDGET[0] <= 0:  # => co-19: rate limit checked FIRST, Example 74's own ordering
        return Response(status=429, headers={"Retry-After": "60"})  # => co-19: 429 -- even a replay, if budget=0
    if idempotency_key in IDEMPOTENCY_STORE:  # => co-18: a REPLAY, reached only when budget still allows it
        return Response(status=200, body=IDEMPOTENCY_STORE[idempotency_key])  # => co-18: the ORIGINAL response
    remaining_after = REQUEST_BUDGET[0] - 1  # => co-20: the quota state AFTER this call consumes one unit
    REQUEST_BUDGET[0] = remaining_after  # => co-19: consumes budget only for a genuinely new write
    new_id = NEXT_ID[0]  # => a fresh id for a genuinely new article
    article: dict[str, object] = {"id": new_id, "title": title}  # => co-09: matches openapi.yaml's Article
    STORE[new_id] = article  # => writes into the store
    IDEMPOTENCY_STORE[idempotency_key] = article  # => co-18: recorded for any future replay
    NEXT_ID[0] += 1  # => advances the counter for the NEXT genuinely new article
    headers = {"RateLimit": f"limit=3, remaining={remaining_after}"}  # => co-20: exposes CURRENT quota state
    return Response(status=201, headers=headers, body=article)  # => 201, with the quota state attached


call_1 = create_article_v1_rate_limited("cap-limit-1", "First")  # => call 1: budget 3 -> 2
print(f"call 1: status={call_1.status}, headers={call_1.headers}")  # => Output: 201, remaining=2

replay_1 = create_article_v1_rate_limited("cap-limit-1", "First")  # => co-18: replays "cap-limit-1" -- budget=2
print(f"replay of call 1 (budget still available): status={replay_1.status}")  # => Output: 200, budget UNCHANGED

call_2 = create_article_v1_rate_limited("cap-limit-2", "Second")  # => call 2: budget 2 -> 1
print(f"call 2: status={call_2.status}, headers={call_2.headers}")  # => Output: 201, remaining=1

call_3 = create_article_v1_rate_limited("cap-limit-3", "Third")  # => call 3: budget 1 -> 0
print(f"call 3: status={call_3.status}, headers={call_3.headers}")  # => Output: 201, remaining=0

over_limit = create_article_v1_rate_limited("cap-limit-4", "Fourth")  # => call 4: budget exhausted
print(f"over-limit call: status={over_limit.status}, headers={over_limit.headers}")  # => Output: 429

replay_after_limit = create_article_v1_rate_limited("cap-limit-1", "First")  # => co-19: budget=0, checked FIRST
print(f"replay after budget exhausted: status={replay_after_limit.status}")  # => Output: 429 -- co-19 wins

compliant_caller_succeeded = call_1.status == 201 and call_2.status == 201 and call_3.status == 201  # => co-19
replay_never_consumed_budget = replay_1.status == 200 and REQUEST_BUDGET[0] == 0  # => co-18: budget=0 after call_3
over_limit_caller_rejected = over_limit.status == 429 and "Retry-After" in over_limit.headers  # => co-19
print(f"compliant callers succeeded: {compliant_caller_succeeded}")  # => Output: True
print(f"replay never consumed budget: {replay_never_consumed_budget}")  # => Output: True
print(f"over-limit caller rejected with Retry-After: {over_limit_caller_rejected}")  # => Output: True

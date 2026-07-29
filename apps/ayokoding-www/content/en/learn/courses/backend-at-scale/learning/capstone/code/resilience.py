# pyright: strict
"""Capstone Step 3: structured logging + rate limiting + a cache layer. (co-20, co-21, co-25)

Layers three production concerns onto the service: structured JSON logs
carrying a correlation id (co-25), a token-bucket rate limit returning 429 +
Retry-After (co-20), and a cache-aside layer that avoids a DB hit on a warm
read (co-21). Verifies logs are structured, the rate limit returns 429, and a
cached read avoids a DB hit.
"""

import json  # => stdlib: structured log lines are JSON
from dataclasses import dataclass, field  # => field: mutable-default-safe factories

LOGS: list[str] = []  # => collects the request's structured log lines
DB_QUERY_COUNT = [
    0
]  # => an instrumented DB counter -- a cached read must NOT increment this
DB: dict[int, dict[str, object]] = {
    1: {"id": 1, "title": "Hello, Capstone"}
}  # => the source of truth
CACHE: dict[int, dict[str, object]] = {}  # => co-21: the cache-aside layer
BUDGET = [3]  # => co-20: a token-bucket budget (3 writes allowed)


def log(
    level: str, message: str, request_id: str
) -> None:  # => co-25: a structured JSON line
    LOGS.append(
        json.dumps({"level": level, "message": message, "request_id": request_id})
    )  # => typed fields


@dataclass  # => the response shape
class Response:
    status: int  # => the HTTP status code
    headers: dict[str, str] = field(
        default_factory=dict[str, str]
    )  # => carries Retry-After on a 429
    body: dict[str, object] = field(
        default_factory=dict[str, object]
    )  # => resource or error payload


def read_cached(
    request_id: str, item_id: int
) -> Response:  # => GET /v1/articles/{id} -- cache-aside
    if item_id in CACHE:  # => co-21: HIT -> no DB query
        log("info", f"cache hit for {item_id}", request_id)  # => co-25: structured log
        return Response(
            200, body={"source": "cache", **CACHE[item_id]}
        )  # => served from cache
    DB_QUERY_COUNT[0] += 1  # => co-21: MISS -> one DB query
    value = DB.get(item_id)  # => the DB read
    log(
        "info", f"cache miss for {item_id} (db query)", request_id
    )  # => co-25: structured log
    if value is None:  # => not found
        return Response(404, {"error": "not found"})  # => 404
    CACHE[item_id] = value  # => co-21: populate
    return Response(200, body={"source": "db", **value})  # => served from DB


def create_rate_limited(
    request_id: str, title: str
) -> Response:  # => POST -- rate-limited
    if BUDGET[0] <= 0:  # => co-20: over the limit -> 429 + Retry-After
        log("warn", "rate limit exceeded", request_id)  # => co-25: structured log
        return Response(
            429, headers={"Retry-After": "60"}, body={"error": "too many requests"}
        )  # => 429
    BUDGET[0] -= 1  # => consume one token
    log("info", f"created article {title!r}", request_id)  # => co-25: structured log
    return Response(
        201, body={"created": title, "budget_remaining": BUDGET[0]}
    )  # => 201


rid = "req-cap-3"  # => the correlation id threaded through every log line (co-25)

# Cache-aside: first read MISSES (db query), second read HITS (no query).
read1 = read_cached(rid, 1)  # => co-21: MISS -> db, DB_QUERY_COUNT=1
read2 = read_cached(rid, 1)  # => co-21: HIT -> cache, DB_QUERY_COUNT stays 1
print(
    f"read 1: source={read1.body['source']}, db_queries={DB_QUERY_COUNT[0]}"
)  # => Output: db, 1
print(
    f"read 2: source={read2.body['source']}, db_queries={DB_QUERY_COUNT[0]}"
)  # => Output: cache, 1

# Rate limit: 3 compliant creates succeed, the 4th trips 429.
c1 = create_rate_limited(rid, "a")  # => budget 3->2
c2 = create_rate_limited(rid, "b")  # => budget 2->1
c3 = create_rate_limited(rid, "c")  # => budget 1->0
c4 = create_rate_limited(rid, "d")  # => co-20: budget 0 -> 429
print(
    f"creates: {[c.status for c in (c1, c2, c3, c4)]}, 4th Retry-After={c4.headers.get('Retry-After')}"
)  # => Output: 201,201,201,429

structured = all(
    set(json.loads(line).keys()) == {"level", "message", "request_id"} for line in LOGS
)  # => co-25
all_carry_id = all(json.loads(line)["request_id"] == rid for line in LOGS)  # => co-25
print(
    f"logs structured: {structured}, all carry correlation id: {all_carry_id}"
)  # => Output: True, True

assert (
    read1.body["source"] == "db"
    and read2.body["source"] == "cache"
    and DB_QUERY_COUNT[0] == 1
)  # => co-21
assert [c.status for c in (c1, c2, c3, c4)] == [201, 201, 201, 429] and c4.headers[
    "Retry-After"
] == "60"  # => co-20
assert structured and all_carry_id  # => co-25: structured logs with a correlation id

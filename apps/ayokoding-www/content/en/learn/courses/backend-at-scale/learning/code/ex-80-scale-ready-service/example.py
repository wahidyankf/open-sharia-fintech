# pyright: strict
"""Example 80: Scale-ready service -- the assembled end-to-end service. (co-06, co-17, co-21, co-29)

Assemble versioned + cursor-paginated REST, an IDEMPOTENT write (Idempotency-
Key), an RBAC role gate, a token-bucket RATE LIMIT returning 429+Retry-After,
a CACHE-ASIDE layer, and an IDEMPOTENT QUEUE CONSUMER behind one integration
check. This is the capstone-preview assembly: every prior pattern combined in
one self-contained service that passes end to end.
"""

from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => the assembled service's response shape
class Response:
    status: int  # => the HTTP status code
    body: dict[str, object] = field(default_factory=dict[str, object])  # => resource or error payload
    headers: dict[str, str] = field(default_factory=dict[str, str])  # => RateLimit/Retry-After headers


@dataclass  # => co-06/co-17/co-21/co-29: the assembled, scale-ready service
class ScaleReadyService:
    store: dict[int, dict[str, object]] = field(default_factory=lambda: {1: {"id": 1, "title": "seed"}})  # => the DB
    idempotency: dict[str, dict[str, object]] = field(default_factory=dict[str, dict[str, object]])  # => co-06: key -> body
    cache: dict[int, dict[str, object]] = field(default_factory=dict[int, dict[str, object]])  # => co-21: cache-aside
    roles: dict[str, str] = field(default_factory=lambda: {"tok-admin": "admin", "tok-user": "user"})  # => co-17: RBAC
    budget: list[int] = field(default_factory=lambda: [2])  # => co-19: token-bucket budget
    processed_msgs: set[str] = field(default_factory=set[str])  # => co-29: idempotent consumer dedup
    next_id: list[int] = field(default_factory=lambda: [2])  # => the next id a create mints

    def list_v1(self, after_cursor: int | None, limit: int) -> Response:  # => GET /v1/items (cursor pagination)
        ids = sorted(self.store.keys())  # => stable order
        threshold = 0 if after_cursor is None else after_cursor  # => resume point
        page_ids = [i for i in ids if i > threshold][:limit]  # => the page
        return Response(200, {"ids": page_ids, "next_cursor": page_ids[-1] if page_ids else None})  # => paginated

    def create_v1(self, token: str, idempotency_key: str, title: str) -> Response:  # => POST /v1/items
        if self.roles.get(token) != "admin":  # => co-17: RBAC -- only admin may create
            return Response(403, {"error": "forbidden"})  # => 403
        if self.budget[0] <= 0:  # => co-19: rate limit FIRST -> 429
            return Response(429, headers={"Retry-After": "60"}, body={"error": "too many requests"})  # => 429
        if idempotency_key in self.idempotency:  # => co-06: replay -> return original, no double-apply
            return Response(200, body=self.idempotency[idempotency_key])  # => 200, original body
        self.budget[0] -= 1  # => consume budget for a genuinely new write
        new_id = self.next_id[0]  # => mint an id
        item: dict[str, object] = {"id": new_id, "title": title}  # => the new resource
        self.store[new_id] = item  # => persist
        self.cache.pop(new_id, None)  # => co-21: invalidate on write
        self.idempotency[idempotency_key] = item  # => co-06: record for safe replay
        self.next_id[0] += 1  # => advance
        return Response(201, body=item)  # => 201 created

    def read_cached(self, item_id: int) -> Response:  # => GET /v1/items/{id} (cache-aside)
        if item_id in self.cache:  # => co-21: HIT
            return Response(200, body={"source": "cache", **self.cache[item_id]})  # => from cache
        value = self.store.get(item_id)  # => MISS -> DB
        if value is None:  # => not found
            return Response(404, {"error": "not found"})  # => 404
        self.cache[item_id] = value  # => co-21: populate
        return Response(200, body={"source": "db", **value})  # => from DB

    def consume_message(self, msg_id: str, body: str) -> str:  # => co-29: idempotent queue consumer
        if msg_id in self.processed_msgs:  # => duplicate -> skip
            return "skipped"  # => no effect
        self.processed_msgs.add(msg_id)  # => record
        _ = body  # => (the effect would happen here)
        return "applied"  # => applied once


svc = ScaleReadyService()  # => the assembled service
checks: list[bool] = []  # => integration check accumulators

# (1) RBAC: a non-admin is forbidden.
forbidden = svc.create_v1("tok-user", "k-1", "X")  # => co-17: 403
checks.append(forbidden.status == 403)  # => RBAC gate works
print(f"non-admin create: {forbidden.status}")  # => Output: 403

# (2) Idempotent create + replay does not double-apply; rate limit decrements.
first = svc.create_v1("tok-admin", "k-1", "First")  # => co-06: 201, budget 2->1
replay = svc.create_v1("tok-admin", "k-1", "First")  # => co-06: 200, original body, no new item
checks.append(first.status == 201 and replay.status == 200 and len(svc.store) == 2)  # => idempotency works
print(f"create {first.status}, replay {replay.status}, store size {len(svc.store)}")  # => Output: 201, 200, 2

# (3) Rate limit trips on the next genuinely-new write (budget now 0 after first).
second = svc.create_v1("tok-admin", "k-2", "Second")  # => budget 1->0, 201
third = svc.create_v1("tok-admin", "k-3", "Third")  # => co-19: budget 0 -> 429
checks.append(second.status == 201 and third.status == 429 and third.headers.get("Retry-After") == "60")  # => rate limit works
print(f"second {second.status}, third (over limit) {third.status} Retry-After={third.headers.get('Retry-After')}")  # => Output: 201, 429

# (4) Cache-aside: first read misses (db), second read hits (cache).
read1 = svc.read_cached(1)  # => co-21: MISS -> db
read2 = svc.read_cached(1)  # => co-21: HIT -> cache
checks.append(read1.body["source"] == "db" and read2.body["source"] == "cache")  # => cache works
print(f"read 1 source={read1.body['source']}, read 2 source={read2.body['source']}")  # => Output: db, cache

# (5) Idempotent consumer: a duplicate message is applied once.
a = svc.consume_message("m-1", "do work")  # => co-29: applied
b = svc.consume_message("m-1", "do work")  # => co-29: skipped
checks.append(a == "applied" and b == "skipped")  # => consumer idempotency works
print(f"consume m-1 first: {a}, redelivered: {b}")  # => Output: applied, skipped

all_pass = all(checks)  # => the integration check
print(f"END-TO-END: {'PASS' if all_pass else 'FAIL'}")  # => Output: PASS

assert all_pass  # => co-06/co-17/co-21/co-29: the assembled service passes end to end

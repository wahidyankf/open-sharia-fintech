# pyright: strict
"""Example 17: Idempotency-Key Mismatch -- reuse a key with a different body. (co-06)

Reusing a known key with a DIFFERENT request body is a client bug (not a safe
retry). The server REJECTS it rather than silently returning the stale
response or applying the new body. This prevents a key collision from doing
the wrong thing on either side.
"""

from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-06: status plus body or error
class Response:
    status: int  # => the HTTP status code
    body: dict[str, object] = field(default_factory=dict[str, object])  # => resource or error payload


STORE: dict[int, dict[str, object]] = {}  # => the resource store
IDEMPOTENCY_STORE: dict[str, tuple[str, Response]] = {}  # => co-06: key -> (request body hash, response)
NEXT_ID = [1]  # => a mutable counter cell


def create_order(idempotency_key: str, item: str) -> Response:  # => POST /orders -- idempotent + mismatch-checked
    if idempotency_key in IDEMPOTENCY_STORE:  # => key was seen before -- inspect whether the body matches
        seen_body, stored_response = IDEMPOTENCY_STORE[idempotency_key]  # => the original body + response
        if seen_body != item:  # => co-06: SAME key, DIFFERENT body -> client bug, REJECT
            return Response(409, {"error": "idempotency key reused with a different body"})  # => 409, rejected
        return stored_response  # => identical body -> safe replay, return the original
    new_id = NEXT_ID[0]  # => a fresh id for a genuinely new order
    order: dict[str, object] = {"id": new_id, "item": item}  # => the new resource
    STORE[new_id] = order  # => persists it
    response = Response(201, order)  # => the first-call response
    IDEMPOTENCY_STORE[idempotency_key] = (item, response)  # => co-06: record body + response together
    NEXT_ID[0] += 1  # => advances the counter
    return response  # => 201 on first create


first = create_order("key-X", "Widget")  # => genuine new order
print(f"first (Widget):    status={first.status}, body={first.body}")  # => Output: 201, id=1

safe_replay = create_order("key-X", "Widget")  # => SAME key, SAME body -> safe replay
print(f"replay (Widget):   status={safe_replay.status}, body={safe_replay.body}")  # => Output: 200, id=1

mismatch = create_order("key-X", "Gadget")  # => co-06: SAME key, DIFFERENT body -> REJECTED
print(f"mismatch (Gadget): status={mismatch.status}, body={mismatch.body}")  # => Output: 409, rejected

assert first.status == 201 and safe_replay.body == first.body  # => genuine + safe replay
assert mismatch.status == 409  # => co-06: a mismatched reuse is rejected, never applied
assert len(STORE) == 1  # => still only one order -- the mismatch created nothing

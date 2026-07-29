# pyright: strict
"""Example 15: Idempotency-Key -- store and replay. (co-06)

On a first POST the server records key -> response. A REPLAY of the same key
returns the ORIGINAL stored response (200) instead of creating a second
resource. This is Stripe's own prior art: store the first result under the
key, replay returns it -- even a 500. NOTE: the IETF draft
(draft-ietf-httpapi-idempotency-key-header-07) is EXPIRED/lapsed, not an RFC,
so this example follows Stripe prior art, not a lapsed draft.
"""

from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-06: the response shape stored and replayed
class Response:
    status: int  # => 201 on first create, 200 on replay
    body: dict[str, object] = field(default_factory=dict[str, object])  # => the resource representation


STORE: dict[int, dict[str, object]] = {}  # => the resource store
IDEMPOTENCY_STORE: dict[str, dict[str, object]] = {}  # => co-06: key -> the BODY the first call produced
NEXT_ID = [1]  # => a mutable counter cell


def create_order(idempotency_key: str, item: str) -> Response:  # => POST /orders -- idempotent via key
    if idempotency_key in IDEMPOTENCY_STORE:  # => co-06: a REPLAY -- do NOT create a second order
        return Response(status=200, body=IDEMPOTENCY_STORE[idempotency_key])  # => returns the ORIGINAL body, 200 semantics
    new_id = NEXT_ID[0]  # => a fresh id for a genuinely new order
    order: dict[str, object] = {"id": new_id, "item": item}  # => the new resource
    STORE[new_id] = order  # => persists it
    IDEMPOTENCY_STORE[idempotency_key] = order  # => co-06: recorded so a future replay is safe
    NEXT_ID[0] += 1  # => advances the counter for the next genuinely new order
    return Response(status=201, body=order)  # => 201 on first create


first = create_order("client-key-A", "Widget")  # => a genuinely new key -> creates
print(f"first call:  status={first.status}, body={first.body}")  # => Output: 201, id=1

replay = create_order("client-key-A", "Widget")  # => co-06: SAME key -> returns the ORIGINAL response
print(f"replay call: status={replay.status}, body={replay.body}")  # => Output: 200, SAME id=1

assert first.status == 201 and replay.status == 200  # => co-06: first 201, replay 200
assert first.body == replay.body  # => the replay returns the IDENTICAL response
assert len(STORE) == 1  # => only ONE order was created across both calls

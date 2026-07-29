# pyright: strict
"""Example 39: Reusing an Idempotency-Key with a Different Body. (co-18)

Stripe's own prior art rejects a replayed key whose BODY does not match the
original request -- a key means "this exact operation, retried," not "any
operation, deduplicated by key alone."
"""

from dataclasses import dataclass  # => a small typed response record for this example

IDEMPOTENCY_STORE: dict[str, dict[str, object]] = {}  # => co-18: key -> (original request body, response)


@dataclass  # => co-18: status plus either the resource or a mismatch error
class Response:  # => co-18: a mismatch is reported the same way any other rejection is
    status: int  # => the HTTP status code
    body: dict[str, object]  # => the charge, or a mismatch error description


def create_charge(idempotency_key: str, amount: int) -> Response:  # => POST /charges, mismatch-aware
    if idempotency_key in IDEMPOTENCY_STORE:  # => co-18: this key has been used before
        stored = IDEMPOTENCY_STORE[idempotency_key]  # => the ORIGINAL request+response pairing
        if stored["amount"] != amount:  # => co-18: the body genuinely DIFFERS from the original
            mismatch_error: dict[str, object] = {"error": "idempotency key reused with a different request body"}
            return Response(422, mismatch_error)  # => co-18: rejected -- the key means THIS exact body
        return Response(200, stored["response"])  # type: ignore[arg-type]  # => co-18: a genuine replay
    body: dict[str, object] = {"id": 1, "amount": amount, "status": "succeeded"}  # => explicit dict[str, object]
    IDEMPOTENCY_STORE[idempotency_key] = {"amount": amount, "response": body}  # => records BOTH facts
    return Response(status=201, body=body)  # => 201 -- a freshly created charge


first = create_charge("key-xyz-789", 1000)  # => call 1: a new key, amount 1000
print(f"first call: status={first.status}, body={first.body}")  # => Output: 201, amount 1000

mismatch = create_charge("key-xyz-789", 2000)  # => call 2: SAME key, DIFFERENT amount -- co-18's guard
# => mismatch.status is 422 -- the key alone was never enough to deduplicate this call
print(f"mismatch call: status={mismatch.status}, body={mismatch.body}")  # => Output: 422, rejected

genuine_replay = create_charge("key-xyz-789", 1000)  # => call 3: SAME key, SAME amount -- a true replay
print(f"replay call: status={genuine_replay.status}, body={genuine_replay.body}")  # => Output: 200, replayed

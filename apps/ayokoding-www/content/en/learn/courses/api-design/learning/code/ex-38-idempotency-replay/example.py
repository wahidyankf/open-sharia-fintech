# pyright: strict
"""Example 38: Replaying the Same Idempotency-Key. (co-18)

Resending the identical `Idempotency-Key` returns the STORED response
instead of re-executing the write -- a counted side effect (here, a charge
counter) proves the operation applied exactly once, not twice.
"""

from dataclasses import dataclass  # => a small typed response record for this example

IDEMPOTENCY_STORE: dict[str, dict[str, object]] = {}  # => co-18: key -> the response it produced
CHARGE_COUNT = [0]  # => a mutable counter cell -- proves the side effect ran only once


@dataclass  # => co-18: status plus the (possibly replayed) resource body
class Response:
    status: int  # => the HTTP status code
    body: dict[str, object]  # => the charge, whether freshly created or replayed


def create_charge(idempotency_key: str, amount: int) -> Response:  # => POST /charges, idempotency-aware
    if idempotency_key in IDEMPOTENCY_STORE:  # => co-18: a REPLAY -- the key was already used
        return Response(status=200, body=IDEMPOTENCY_STORE[idempotency_key])  # => the STORED response, verbatim
    CHARGE_COUNT[0] += 1  # => co-18: the side effect ONLY runs on a genuinely new key
    body: dict[str, object] = {"id": CHARGE_COUNT[0], "amount": amount, "status": "succeeded"}  # => the real charge
    IDEMPOTENCY_STORE[idempotency_key] = body  # => records it for any FUTURE replay of this same key
    return Response(status=201, body=body)  # => 201 -- a freshly created charge


first = create_charge("key-abc-123", 5000)  # => call 1: a genuinely new key
print(f"first call: status={first.status}, body={first.body}")  # => Output: 201, charge_count=1

replay = create_charge("key-abc-123", 5000)  # => call 2: the SAME key, resent (e.g. after a timeout)
# => replay.body == first.body -- the SAME dict object, not a newly minted one
print(f"replay call: status={replay.status}, body={replay.body}")  # => Output: 200, IDENTICAL body

print(f"total charges actually created: {CHARGE_COUNT[0]}")  # => Output: 1 -- co-18: applied exactly once

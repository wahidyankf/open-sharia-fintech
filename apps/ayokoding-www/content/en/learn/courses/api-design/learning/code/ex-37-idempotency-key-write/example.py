# pyright: strict
"""Example 37: Recording an Idempotency-Key on a Write. (co-18)

An `Idempotency-Key` header (Stripe prior art -- the matching IETF draft is
lapsed) lets a POST be safely retried: the server records the key alongside
the response it produced, the foundation Examples 38-39 build on.
"""

from dataclasses import dataclass  # => a small typed response record for this example

IDEMPOTENCY_STORE: dict[str, dict[str, object]] = {}  # => co-18: key -> the response it produced
# => IDEMPOTENCY_STORE starts empty (type: dict[str, dict[str, object]])


@dataclass  # => co-18: status plus the created resource's own body
class Response:
    status: int  # => the HTTP status code
    body: dict[str, object]  # => the created resource


def create_charge(idempotency_key: str, amount: int) -> Response:  # => POST /charges
    body: dict[str, object] = {"id": 1, "amount": amount, "status": "succeeded"}  # => explicit dict[str, object]
    IDEMPOTENCY_STORE[idempotency_key] = body  # => co-18: records the key -> response pairing
    return Response(status=201, body=body)  # => a normal 201 Created response


response = create_charge(idempotency_key="key-abc-123", amount=5000)  # => the FIRST call with this key
# => response.body is {'id': 1, 'amount': 5000, 'status': 'succeeded'}
print(f"status={response.status}, body={response.body}")  # => Output: 201, the charge just created
print(f"recorded under key: {IDEMPOTENCY_STORE['key-abc-123']}")  # => Output: the same body, stored

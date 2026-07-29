# pyright: strict
"""Example 16: Idempotency-Key -- a retried charge applies ONCE. (co-06)

A retried POST charge with the SAME Idempotency-Key must not double-charge.
This example models a wallet balance: the first call debits and records the
key; a replay returns the original result WITHOUT debiting again.
"""

from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-06: the charge result stored and replayed
class ChargeResult:
    status: int  # => 201 first, 200 replay
    body: dict[str, object] = field(default_factory=dict[str, object])  # => charge id + new balance


BALANCE = [1000]  # => the wallet, mutable so a debit persists across calls
CHARGES: dict[str, dict[str, object]] = {}  # => co-06: idempotency key -> the charge BODY


def charge(idempotency_key: str, amount: int) -> ChargeResult:  # => POST /charges -- debit the wallet
    if idempotency_key in CHARGES:  # => co-06: a REPLAY -> return original body, do NOT debit again
        return ChargeResult(status=200, body=CHARGES[idempotency_key])  # => the original result, untouched
    BALANCE[0] -= amount  # => genuinely new charge -> debit the wallet once
    body: dict[str, object] = {"charged": amount, "balance": BALANCE[0]}  # => the result body
    CHARGES[idempotency_key] = body  # => co-06: recorded so a replay is a no-op
    return ChargeResult(status=201, body=body)  # => 201 on the genuine charge


first = charge("pay-key-1", 250)  # => genuine charge: 1000 -> 750
print(f"first charge:  status={first.status}, body={first.body}")  # => Output: 201, balance 750

replay = charge("pay-key-1", 250)  # => co-06: retry after a timeout -- SAME key, no second debit
print(f"replay charge: status={replay.status}, body={replay.body}")  # => Output: 200, balance still 750

second = charge("pay-key-2", 100)  # => a DIFFERENT key -> a genuinely new charge
print(f"second charge: status={second.status}, body={second.body}")  # => Output: 201, balance 650

assert BALANCE[0] == 650  # => co-06: debited exactly 250 + 100 = 350, the replay did NOT double-charge
assert first.body["balance"] == replay.body["balance"]  # => replay returned the original result unchanged

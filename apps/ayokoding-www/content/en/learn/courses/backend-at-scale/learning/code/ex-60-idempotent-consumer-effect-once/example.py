# pyright: strict
"""Example 60: Idempotent consumer -- a side effect happens exactly once. (co-29)

A side-effecting message (e.g. incrementing a balance) is delivered MULTIPLE
times. The idempotent consumer applies the EFFECT exactly once by deduping
on the message id, so the balance increments once despite N redeliveries.
"""

from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-29: a credit message carrying an idempotent id + an amount
class Credit:
    id: str  # => the dedup key
    amount: int  # => how much to add to the balance


BALANCE = [0]  # => the side-effect target (a wallet balance)


@dataclass  # => co-29: a consumer that guards the side effect with an id set
class CreditConsumer:
    processed: set[str] = field(default_factory=set[str])  # => ids whose effect was already applied

    def apply(self, credit: Credit) -> bool:  # => returns True if the effect was applied, False if deduped
        if credit.id in self.processed:  # => co-29: duplicate -> skip the side effect
            return False  # => no balance change
        self.processed.add(credit.id)  # => record the id
        BALANCE[0] += credit.amount  # => apply the side effect ONCE
        return True  # => applied


consumer = CreditConsumer()  # => co-29: guards the balance mutation
credit = Credit(id="credit-1", amount=100)  # => the original message

# The broker delivers the SAME credit 4 times (at-least-once, retries).
results = [consumer.apply(credit) for _ in range(4)]  # => co-29: applied once, deduped 3 times
print(f"deliveries: {len(results)}, applied count: {sum(results)}")  # => Output: 4 deliveries, 1 applied
print(f"final balance: {BALANCE[0]}")  # => Output: 100 -- incremented ONCE despite 4 deliveries

assert results == [True, False, False, False]  # => co-29: effect applied exactly once
assert BALANCE[0] == 100  # => the side effect happened once, not four times

# => Keeps this domain step explicit and reviewable.
"""Example 45: event payloads carry only facts consumers need."""

# => Keeps the artifact runnable with explicit dependencies.
from dataclasses import dataclass


# => Uses generated value behaviour so policy is not duplicated.
@dataclass(frozen=True)
# => Gives domain rules a single, named home.
class OrderPlaced:
    # => Keeps this domain step explicit and reviewable.
    order_id: str
    amount: int  # => the amount was true when this event happened


# => Keeps scenario data close to the rule it exercises.
event = OrderPlaced("o-1", 25)
# => Proves the stated business rule is observable.
assert (event.order_id, event.amount) == ("o-1", 25)

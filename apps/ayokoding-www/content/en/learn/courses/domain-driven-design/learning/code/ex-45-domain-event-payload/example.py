"""Example 45: event payloads carry only facts consumers need."""

from dataclasses import dataclass


@dataclass(frozen=True)
class OrderPlaced:
    order_id: str
    amount: int  # => the amount was true when this event happened


event = OrderPlaced("o-1", 25)
assert (event.order_id, event.amount) == ("o-1", 25)

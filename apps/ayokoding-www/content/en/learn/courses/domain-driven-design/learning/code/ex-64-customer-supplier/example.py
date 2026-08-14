# => Keeps this domain step explicit and reviewable.
"""Example 64: upstream publishes the downstream's needed contract."""

# => Keeps the artifact runnable with explicit dependencies.
from dataclasses import dataclass


# => Uses generated value behaviour so policy is not duplicated.
@dataclass(frozen=True)
# => Gives domain rules a single, named home.
class ShipmentRequested:
    # => Keeps this domain step explicit and reviewable.
    order_id: str
    destination: str  # => agreed published language


# => Names policy so callers do not recreate the rule.
def orders_publish() -> ShipmentRequested:
    # => Returns the domain result instead of leaking representation.
    return ShipmentRequested("o-1", "Jakarta")


# => Names policy so callers do not recreate the rule.
def shipping_consume(event: ShipmentRequested) -> str:
    return event.destination  # => downstream consumes contract


# => Proves the stated business rule is observable.
assert shipping_consume(orders_publish()) == "Jakarta"

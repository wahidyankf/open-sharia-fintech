# => Keeps this domain step explicit and reviewable.
"""Example 80: assemble values, a root, event, port-shaped adapter, and ACL."""

# => Keeps the artifact runnable with explicit dependencies.
from dataclasses import dataclass


# => Uses generated value behaviour so policy is not duplicated.
@dataclass(frozen=True)
# => Gives domain rules a single, named home.
class Quantity:
    value: int  # => immutable domain value


# => Gives domain rules a single, named home.
class Order:
    # => Establishes valid state before callers can rely on it.
    def __init__(self, limit: int) -> None:
        # => Keeps lifecycle state controlled by the domain object.
        self.limit, self.total, self.events = limit, 0, []

    # => Names policy so callers do not recreate the rule.
    def add(self, amount: int) -> None:
        # => Checks policy before a state change is allowed.
        if self.total + amount > self.limit:
            raise ValueError("credit limit")  # => root protects invariant
        # => Keeps lifecycle state controlled by the domain object.
        self.total += amount
        self.events.append("OrderPlaced")  # => valid transition emits a fact


# => Names policy so callers do not recreate the rule.
def sales_to_shipping(order_id: str, quantity: Quantity) -> dict[str, object]:
    # => Returns the domain result instead of leaking representation.
    return {
        # => Keeps this domain step explicit and reviewable.
        "sales_order_id": order_id,
        # => Keeps this domain step explicit and reviewable.
        "quantity": quantity.value,
    }  # => ACL publishes a translated edge model


# => Keeps scenario data close to the rule it exercises.
order = Order(10)
# => Keeps this domain step explicit and reviewable.
order.add(5)
# => Proves the stated business rule is observable.
assert (
    # => Keeps this domain step explicit and reviewable.
    order.total == 5
    # => Keeps this domain step explicit and reviewable.
    and order.events == ["OrderPlaced"]
    # => Keeps this domain step explicit and reviewable.
    and sales_to_shipping("o-1", Quantity(1))["quantity"] == 1
    # => Keeps this domain step explicit and reviewable.
)

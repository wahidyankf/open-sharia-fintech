"""Example 80: assemble values, a root, event, port-shaped adapter, and ACL."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Quantity:
    value: int  # => immutable domain value


class Order:
    def __init__(self, limit: int) -> None:
        self.limit, self.total, self.events = limit, 0, []

    def add(self, amount: int) -> None:
        if self.total + amount > self.limit:
            raise ValueError("credit limit")  # => root protects invariant
        self.total += amount
        self.events.append("OrderPlaced")  # => valid transition emits a fact


def sales_to_shipping(order_id: str, quantity: Quantity) -> dict[str, object]:
    return {
        "sales_order_id": order_id,
        "quantity": quantity.value,
    }  # => ACL publishes a translated edge model


order = Order(10)
order.add(5)
assert (
    order.total == 5
    and order.events == ["OrderPlaced"]
    and sales_to_shipping("o-1", Quantity(1))["quantity"] == 1
)

"""Example 64: upstream publishes the downstream's needed contract."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ShipmentRequested:
    order_id: str
    destination: str  # => agreed published language


def orders_publish() -> ShipmentRequested:
    return ShipmentRequested("o-1", "Jakarta")


def shipping_consume(event: ShipmentRequested) -> str:
    return event.destination  # => downstream consumes contract


assert shipping_consume(orders_publish()) == "Jakarta"

"""Example 77: a shipment stores the foreign order's identity only."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Shipment:
    sales_order_id: str  # => Shipping does not import the Sales Order aggregate
    destination: str


assert Shipment("o-1", "Jakarta").sales_order_id == "o-1"

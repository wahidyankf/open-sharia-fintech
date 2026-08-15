# => Keeps this domain step explicit and reviewable.
"""Example 77: a shipment stores the foreign order's identity only."""

# => Keeps the artifact runnable with explicit dependencies.
from dataclasses import dataclass


# => Uses generated value behaviour so policy is not duplicated.
@dataclass(frozen=True)
# => Gives domain rules a single, named home.
class Shipment:
    sales_order_id: str  # => Shipping does not import the Sales Order aggregate
    # => Keeps this domain step explicit and reviewable.
    destination: str


# => Proves the stated business rule is observable.
assert Shipment("o-1", "Jakarta").sales_order_id == "o-1"

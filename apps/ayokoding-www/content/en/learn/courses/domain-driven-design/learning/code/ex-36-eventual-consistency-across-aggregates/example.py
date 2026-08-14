# => Keeps this domain step explicit and reviewable.
"""Example 36: inventory converges after an order event."""


# => Gives domain rules a single, named home.
class Inventory:
    # => Establishes valid state before callers can rely on it.
    def __init__(self, available: int) -> None:
        # => Keeps lifecycle state controlled by the domain object.
        self.available = available

    # => Names policy so callers do not recreate the rule.
    def on_order_placed(self, quantity: int) -> None:
        self.available -= quantity  # => later handler updates its root


inventory = Inventory(5)  # => inventory begins independently from the order
inventory.on_order_placed(2)  # => an event handler performs eventual work
# => Proves the stated business rule is observable.
assert inventory.available == 3

"""Example 36: inventory converges after an order event."""


class Inventory:
    def __init__(self, available: int) -> None:
        self.available = available

    def on_order_placed(self, quantity: int) -> None:
        self.available -= quantity  # => later handler updates its root


inventory = Inventory(5)  # => inventory begins independently from the order
inventory.on_order_placed(2)  # => an event handler performs eventual work
assert inventory.available == 3

"""Example 48: an event handler updates its own aggregate."""


class Inventory:
    def __init__(self, quantity: int) -> None:
        self.quantity = quantity

    def reserve(self, event: dict[str, int]) -> None:
        self.quantity -= event["quantity"]  # => handler owns inventory rule


inventory = Inventory(4)
inventory.reserve({"quantity": 1})
assert inventory.quantity == 3

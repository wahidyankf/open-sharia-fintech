# => Keeps this domain step explicit and reviewable.
"""Example 48: an event handler updates its own aggregate."""


# => Gives domain rules a single, named home.
class Inventory:
    # => Establishes valid state before callers can rely on it.
    def __init__(self, quantity: int) -> None:
        # => Keeps lifecycle state controlled by the domain object.
        self.quantity = quantity

    # => Names policy so callers do not recreate the rule.
    def reserve(self, event: dict[str, int]) -> None:
        self.quantity -= event["quantity"]  # => handler owns inventory rule


# => Keeps scenario data close to the rule it exercises.
inventory = Inventory(4)
# => Keeps this domain step explicit and reviewable.
inventory.reserve({"quantity": 1})
# => Proves the stated business rule is observable.
assert inventory.quantity == 3

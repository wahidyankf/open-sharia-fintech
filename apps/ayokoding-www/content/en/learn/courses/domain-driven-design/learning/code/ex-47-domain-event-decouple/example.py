# => Keeps this domain step explicit and reviewable.
"""Example 47: a root knows an event name, not its consumers."""


# => Gives domain rules a single, named home.
class Order:
    # => Establishes valid state before callers can rely on it.
    def __init__(self) -> None:
        # => Keeps lifecycle state controlled by the domain object.
        self.events: list[str] = []

    # => Names policy so callers do not recreate the rule.
    def place(self) -> None:
        # => Keeps lifecycle state controlled by the domain object.
        self.events.append(
            # => Keeps this domain step explicit and reviewable.
            "OrderPlaced"
        )  # => no Inventory import or handler field exists


# => Keeps scenario data close to the rule it exercises.
order = Order()
# => Keeps this domain step explicit and reviewable.
order.place()
# => Proves the stated business rule is observable.
assert not hasattr(order, "inventory") and order.events == ["OrderPlaced"]

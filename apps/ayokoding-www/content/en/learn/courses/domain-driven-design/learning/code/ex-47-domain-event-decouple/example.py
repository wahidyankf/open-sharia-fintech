"""Example 47: a root knows an event name, not its consumers."""


class Order:
    def __init__(self) -> None:
        self.events: list[str] = []

    def place(self) -> None:
        self.events.append(
            "OrderPlaced"
        )  # => no Inventory import or handler field exists


order = Order()
order.place()
assert not hasattr(order, "inventory") and order.events == ["OrderPlaced"]

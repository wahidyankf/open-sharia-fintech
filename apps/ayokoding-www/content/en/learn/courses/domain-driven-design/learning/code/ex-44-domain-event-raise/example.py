"""Example 44: a root records an event after its transition."""


class Order:
    def __init__(self) -> None:
        self.pending_events: list[str] = []

    def place(self) -> None:
        self.pending_events.append("OrderPlaced")  # => root records the domain fact


order = Order()
order.place()
assert order.pending_events == ["OrderPlaced"]

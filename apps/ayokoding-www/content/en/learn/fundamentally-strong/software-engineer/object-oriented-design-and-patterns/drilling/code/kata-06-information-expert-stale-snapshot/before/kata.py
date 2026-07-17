"""Kata 6 (before): GRASP Information Expert violation -- OrderPrinter computes the total instead of Order, and goes stale."""


class Order:
    def __init__(self) -> None:
        self.items: list[float] = []

    def add_item(self, price: float) -> None:
        self.items.append(price)


class OrderPrinter:  # SMELL: computes a total from a SNAPSHOT, not from Order itself (which actually owns the data)
    def __init__(self, order: Order) -> None:
        self.snapshot = list(order.items)  # captured once, at construction time

    def total(self) -> float:
        return sum(self.snapshot)


order = Order()
order.add_item(10.0)
printer = OrderPrinter(order)
order.add_item(20.0)  # added AFTER the printer was built
print(printer.total())  # expected 30.0 -- but the printer's stale snapshot never saw the second item

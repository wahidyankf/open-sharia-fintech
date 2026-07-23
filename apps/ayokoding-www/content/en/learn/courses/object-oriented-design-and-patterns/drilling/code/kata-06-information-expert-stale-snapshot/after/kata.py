"""Kata 6 (after): GRASP Information Expert -- Order computes its own total, always reading its CURRENT items."""


class Order:  # => co-06: Order owns items, so Order is the natural information expert for the total
    def __init__(self) -> None:
        self.items: list[float] = []

    def add_item(self, price: float) -> None:
        self.items.append(price)

    def total(self) -> float:
        return sum(self.items)  # => always reads CURRENT state, never a stale snapshot


order = Order()
order.add_item(10.0)
order.add_item(20.0)
print(order.total())

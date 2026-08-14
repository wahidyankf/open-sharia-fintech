"""Example 29: an order contains its own lines."""


class Order:
    def __init__(self) -> None:
        self._lines: list[int] = []  # => child state belongs to one root

    def add_line(self, price: int) -> None:
        self._lines.append(price)  # => enter only through the root

    def total(self) -> int:
        return sum(self._lines)  # => root sees every child


order = Order()
order.add_line(10)
assert order.total() == 10

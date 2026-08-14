"""Example 25: move a leaked rule into the root."""


class Order:
    def __init__(self, lines: list[int]) -> None:
        self._lines = lines

    def add_line(self, price: int) -> None:
        if price <= 0:
            raise ValueError(
                "price must be positive"
            )  # => the root guards its own state
        self._lines.append(price)


order = Order([])
order.add_line(20)
assert order._lines == [20]  # => an application service only needs to orchestrate

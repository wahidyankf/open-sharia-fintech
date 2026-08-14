"""Example 31: the root checks a child collection invariant."""


class Order:
    def __init__(self, credit_limit: int) -> None:
        self.limit, self._lines = credit_limit, []

    def add_line(self, price: int) -> None:
        if sum(self._lines) + price > self.limit:
            raise ValueError("credit limit")  # => check whole aggregate
        self._lines.append(price)


order = Order(10)
order.add_line(6)
try:
    order.add_line(5)
except ValueError:
    pass  # => rejected child keeps the aggregate valid
assert order._lines == [6]

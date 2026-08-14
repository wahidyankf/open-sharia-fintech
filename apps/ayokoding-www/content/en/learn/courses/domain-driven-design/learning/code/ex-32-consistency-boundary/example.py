"""Example 32: validate first, then replace aggregate state."""


class Order:
    def __init__(self) -> None:
        self._lines = [1]

    def replace_lines(self, lines: list[int]) -> None:
        if not lines or any(price <= 0 for price in lines):
            raise ValueError("valid lines required")  # => atomic guard
        self._lines = lines[:]  # => only a complete valid collection is stored


order = Order()
try:
    order.replace_lines([1, 0])
except ValueError:
    pass
assert order._lines == [1]  # => no partial persistence

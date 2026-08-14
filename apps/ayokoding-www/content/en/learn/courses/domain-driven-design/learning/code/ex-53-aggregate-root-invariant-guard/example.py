"""Example 53: no public child mutation bypasses the root."""


class Order:
    def __init__(self) -> None:
        self.__lines: list[int] = []  # => name mangling keeps the collection private

    def add_line(self, price: int) -> None:
        if price <= 0:
            raise ValueError("positive price")  # => root owns the guard
        self.__lines.append(price)

    def line_count(self) -> int:
        return len(self.__lines)


order = Order()
order.add_line(1)
assert order.line_count() == 1

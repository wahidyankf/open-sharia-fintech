"""Example 30: expose a read-only child view."""


class Order:
    def __init__(self) -> None:
        self._lines: list[str] = []

    def add_line(self, product: str) -> None:
        self._lines.append(product)  # => mutation stays internal

    @property
    def lines(self) -> tuple[str, ...]:
        return tuple(self._lines)  # => callers receive no append method


order = Order()
order.add_line("book")
assert order.lines == ("book",)

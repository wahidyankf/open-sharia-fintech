"""Example 21: a factory assembles an initially valid aggregate."""


class Order:
    def __init__(self, id: str, lines: list[str]) -> None:
        self.id, self._lines = id, lines

    @classmethod
    def create(cls, id: str, first_product: str) -> "Order":
        return cls(
            id, [first_product]
        )  # => no caller can create an empty order accidentally


order = Order.create("o-1", "book")  # => factory coordinates child creation
assert order._lines == ["book"]  # => valid aggregate returned

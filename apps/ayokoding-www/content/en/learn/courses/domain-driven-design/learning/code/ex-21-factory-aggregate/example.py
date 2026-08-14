# => Keeps this domain step explicit and reviewable.
"""Example 21: a factory assembles an initially valid aggregate."""


# => Gives domain rules a single, named home.
class Order:
    # => Establishes valid state before callers can rely on it.
    def __init__(self, id: str, lines: list[str]) -> None:
        # => Keeps lifecycle state controlled by the domain object.
        self.id, self._lines = id, lines

    # => Uses generated value behaviour so policy is not duplicated.
    @classmethod
    # => Names policy so callers do not recreate the rule.
    def create(cls, id: str, first_product: str) -> "Order":
        # => Returns the domain result instead of leaking representation.
        return cls(
            # => Keeps this domain step explicit and reviewable.
            id,
            # => Supplies the required first child so no empty root escapes.
            [first_product],
        )  # => no caller can create an empty order accidentally


order = Order.create("o-1", "book")  # => factory coordinates child creation
assert order._lines == ["book"]  # => valid aggregate returned

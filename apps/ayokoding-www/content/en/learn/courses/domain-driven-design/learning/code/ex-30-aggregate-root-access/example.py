# => Keeps this domain step explicit and reviewable.
"""Example 30: expose a read-only child view."""


# => Gives domain rules a single, named home.
class Order:
    # => Establishes valid state before callers can rely on it.
    def __init__(self) -> None:
        # => Keeps lifecycle state controlled by the domain object.
        self._lines: list[str] = []

    # => Names policy so callers do not recreate the rule.
    def add_line(self, product: str) -> None:
        self._lines.append(product)  # => mutation stays internal

    # => Uses generated value behaviour so policy is not duplicated.
    @property
    # => Names policy so callers do not recreate the rule.
    def lines(self) -> tuple[str, ...]:
        return tuple(self._lines)  # => callers receive no append method


# => Keeps scenario data close to the rule it exercises.
order = Order()
# => Keeps this domain step explicit and reviewable.
order.add_line("book")
# => Proves the stated business rule is observable.
assert order.lines == ("book",)

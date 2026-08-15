# => Keeps this domain step explicit and reviewable.
"""Example 29: an order contains its own lines."""


# => Gives domain rules a single, named home.
class Order:
    # => Establishes valid state before callers can rely on it.
    def __init__(self) -> None:
        self._lines: list[int] = []  # => child state belongs to one root

    # => Names policy so callers do not recreate the rule.
    def add_line(self, price: int) -> None:
        self._lines.append(price)  # => enter only through the root

    # => Names policy so callers do not recreate the rule.
    def total(self) -> int:
        return sum(self._lines)  # => root sees every child


# => Keeps scenario data close to the rule it exercises.
order = Order()
# => Keeps this domain step explicit and reviewable.
order.add_line(10)
# => Proves the stated business rule is observable.
assert order.total() == 10

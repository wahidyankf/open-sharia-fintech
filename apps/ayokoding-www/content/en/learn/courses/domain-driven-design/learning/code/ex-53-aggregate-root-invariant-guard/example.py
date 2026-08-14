# => Keeps this domain step explicit and reviewable.
"""Example 53: no public child mutation bypasses the root."""


# => Gives domain rules a single, named home.
class Order:
    # => Establishes valid state before callers can rely on it.
    def __init__(self) -> None:
        self.__lines: list[int] = []  # => name mangling keeps the collection private

    # => Names policy so callers do not recreate the rule.
    def add_line(self, price: int) -> None:
        # => Checks policy before a state change is allowed.
        if price <= 0:
            raise ValueError("positive price")  # => root owns the guard
        # => Keeps lifecycle state controlled by the domain object.
        self.__lines.append(price)

    # => Names policy so callers do not recreate the rule.
    def line_count(self) -> int:
        # => Returns the domain result instead of leaking representation.
        return len(self.__lines)


# => Keeps scenario data close to the rule it exercises.
order = Order()
# => Keeps this domain step explicit and reviewable.
order.add_line(1)
# => Proves the stated business rule is observable.
assert order.line_count() == 1

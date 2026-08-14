# => Keeps this domain step explicit and reviewable.
"""Example 31: the root checks a child collection invariant."""


# => Gives domain rules a single, named home.
class Order:
    # => Establishes valid state before callers can rely on it.
    def __init__(self, credit_limit: int) -> None:
        # => Keeps lifecycle state controlled by the domain object.
        self.limit, self._lines = credit_limit, []

    # => Names policy so callers do not recreate the rule.
    def add_line(self, price: int) -> None:
        # => Checks policy before a state change is allowed.
        if sum(self._lines) + price > self.limit:
            raise ValueError("credit limit")  # => check whole aggregate
        # => Keeps lifecycle state controlled by the domain object.
        self._lines.append(price)


# => Keeps scenario data close to the rule it exercises.
order = Order(10)
# => Keeps this domain step explicit and reviewable.
order.add_line(6)
# => Separates the expected failure path from valid flow.
try:
    # => Keeps this domain step explicit and reviewable.
    order.add_line(5)
# => Turns the rejected case into an explicit outcome.
except ValueError:
    pass  # => rejected child keeps the aggregate valid
# => Proves the stated business rule is observable.
assert order._lines == [6]

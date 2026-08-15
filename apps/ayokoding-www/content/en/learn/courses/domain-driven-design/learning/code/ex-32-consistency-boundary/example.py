# => Keeps this domain step explicit and reviewable.
"""Example 32: validate first, then replace aggregate state."""


# => Gives domain rules a single, named home.
class Order:
    # => Establishes valid state before callers can rely on it.
    def __init__(self) -> None:
        # => Keeps lifecycle state controlled by the domain object.
        self._lines = [1]

    # => Names policy so callers do not recreate the rule.
    def replace_lines(self, lines: list[int]) -> None:
        # => Checks policy before a state change is allowed.
        if not lines or any(price <= 0 for price in lines):
            raise ValueError("valid lines required")  # => atomic guard
        self._lines = lines[:]  # => only a complete valid collection is stored


# => Keeps scenario data close to the rule it exercises.
order = Order()
# => Separates the expected failure path from valid flow.
try:
    # => Keeps this domain step explicit and reviewable.
    order.replace_lines([1, 0])
# => Turns the rejected case into an explicit outcome.
except ValueError:
    # => Keeps this domain step explicit and reviewable.
    pass
assert order._lines == [1]  # => no partial persistence

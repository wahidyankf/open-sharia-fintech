# => Keeps this domain step explicit and reviewable.
"""Example 25: move a leaked rule into the root."""


# => Gives domain rules a single, named home.
class Order:
    # => Establishes valid state before callers can rely on it.
    def __init__(self, lines: list[int]) -> None:
        # => Keeps lifecycle state controlled by the domain object.
        self._lines = lines

    # => Names policy so callers do not recreate the rule.
    def add_line(self, price: int) -> None:
        # => Checks policy before a state change is allowed.
        if price <= 0:
            # => Stops invalid business state at the boundary.
            raise ValueError(
                # => Keeps this domain step explicit and reviewable.
                "price must be positive"
            )  # => the root guards its own state
        # => Keeps lifecycle state controlled by the domain object.
        self._lines.append(price)


# => Keeps scenario data close to the rule it exercises.
order = Order([])
# => Keeps this domain step explicit and reviewable.
order.add_line(20)
assert order._lines == [20]  # => an application service only needs to orchestrate

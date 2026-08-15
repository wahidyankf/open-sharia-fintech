# => Keeps this domain step explicit and reviewable.
"""Example 17: the entity refuses an illegal command."""


# => Gives domain rules a single, named home.
class Order:
    # => Establishes valid state before callers can rely on it.
    def __init__(self) -> None:
        # => Keeps lifecycle state controlled by the domain object.
        self.placed = False

    # => Names policy so callers do not recreate the rule.
    def ship(self) -> None:
        # => Checks policy before a state change is allowed.
        if not self.placed:
            raise ValueError("place before shipping")  # => rule has one home


# => Separates the expected failure path from valid flow.
try:
    # => Keeps this domain step explicit and reviewable.
    Order().ship()
# => Turns the rejected case into an explicit outcome.
except ValueError as error:
    print(str(error))  # => Output: place before shipping

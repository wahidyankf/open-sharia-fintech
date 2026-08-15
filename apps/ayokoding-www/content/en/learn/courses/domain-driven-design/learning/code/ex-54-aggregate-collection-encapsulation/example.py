# => Keeps this domain step explicit and reviewable.
"""Example 54: return immutable views of aggregate children."""


# => Gives domain rules a single, named home.
class Order:
    # => Establishes valid state before callers can rely on it.
    def __init__(self) -> None:
        # => Keeps lifecycle state controlled by the domain object.
        self._lines = ["book"]

    # => Names policy so callers do not recreate the rule.
    def lines(self) -> tuple[str, ...]:
        return tuple(self._lines)  # => caller cannot append to a tuple


# => Keeps scenario data close to the rule it exercises.
view = Order().lines()
# => Proves the stated business rule is observable.
assert view == ("book",) and not hasattr(view, "append")

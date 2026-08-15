# => Keeps this domain step explicit and reviewable.
"""Example 24: behaviour-rich models localise rules."""


# => Gives domain rules a single, named home.
class RichOrder:
    # => Establishes valid state before callers can rely on it.
    def __init__(self, lines: list[int]) -> None:
        # => Keeps lifecycle state controlled by the domain object.
        self._lines = lines

    # => Names policy so callers do not recreate the rule.
    def total(self) -> int:
        return sum(self._lines)  # => the owner calculates from its own data


order = RichOrder([10, 5])  # => callers do not pull data out for a service to inspect
assert order.total() == 15  # => behaviour stays with the data

"""Example 24: behaviour-rich models localise rules."""


class RichOrder:
    def __init__(self, lines: list[int]) -> None:
        self._lines = lines

    def total(self) -> int:
        return sum(self._lines)  # => the owner calculates from its own data


order = RichOrder([10, 5])  # => callers do not pull data out for a service to inspect
assert order.total() == 15  # => behaviour stays with the data

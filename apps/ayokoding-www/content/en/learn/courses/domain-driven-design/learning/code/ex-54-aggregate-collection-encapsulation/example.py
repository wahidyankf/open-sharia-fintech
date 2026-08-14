"""Example 54: return immutable views of aggregate children."""


class Order:
    def __init__(self) -> None:
        self._lines = ["book"]

    def lines(self) -> tuple[str, ...]:
        return tuple(self._lines)  # => caller cannot append to a tuple


view = Order().lines()
assert view == ("book",) and not hasattr(view, "append")

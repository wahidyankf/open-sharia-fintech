"""Example 18: Dataflow Two Cells."""

from collections.abc import Callable


class Cell:  # => a spreadsheet-style cell: either a raw value, or a formula over another cell
    def __init__(self, compute: Callable[[], int]) -> None:  # => every cell is defined by HOW to compute it
        self._compute: Callable[[], int] = compute  # => the recompute rule, called fresh each read
        self.value: int = compute()  # => cache the initial computed value

    def recompute(self) -> None:  # => re-run this cell's rule and refresh its cached value
        self.value = self._compute()  # => the recompute rule reads whatever it currently depends on


a = Cell(lambda: 1)  # => cell A: a plain value with no dependency, starts at 1
b = Cell(lambda: a.value + 1)  # => cell B: a FORMULA over A -- always "A's current value, plus one"

print(a.value, b.value)  # => B was computed once at construction time, from A's starting value
# => Output: 1 2

a.value = 10  # => write directly to A's cached value (simulating "the user edited cell A")
print(a.value, b.value)  # => B has NOT recomputed yet -- nothing pushed the change automatically here
# => Output: 10 2

b.recompute()  # => explicitly recompute B FROM A's now-current value -- the dataflow edge fires
print(a.value, b.value)  # => B now reflects A's new value: 10 + 1 = 11
# => Output: 10 11

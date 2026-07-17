"""Example 41: Reactive Derived Value."""

from collections.abc import Callable  # => types every no-argument callback stored below


class Signal:  # => a reactive source value that notifies dependents automatically
    def __init__(self, initial: int) -> None:  # => constructor seeds the starting value
        self._value = initial  # => the current value, hidden behind get()/set() below
        self._on_change: list[Callable[[], None]] = []  # => callbacks to run whenever this signal changes

    def get(self) -> int:  # => read the current value
        return self._value  # => a plain read -- getting never triggers propagation

    def set(self, value: int) -> None:  # => write a new value and PUSH the change to every dependent
        self._value = value  # => update the internal box first
        for callback in self._on_change:  # => automatically notify -- no dependent has to poll
            callback()  # => runs the dependent's recompute hook synchronously, right here

    def on_change(self, callback: Callable[[], None]) -> None:  # => register a dependent's recompute hook
        self._on_change.append(callback)  # => append only -- does NOT call callback with the current value


class Computed:  # => a derived signal: recomputes automatically whenever a source changes
    def __init__(self, compute: Callable[[], int], *sources: Signal) -> None:  # => wires up every source
        self._compute = compute  # => the formula, e.g. "a.get() + b.get()"
        self.value = compute()  # => compute once immediately, so `c` is correct before any update
        for source in sources:  # => subscribe to EVERY source this computed value depends on
            source.on_change(self._recompute)  # => wire automatic propagation

    def _recompute(self) -> None:  # => runs automatically whenever ANY source signal changes
        self.value = self._compute()  # => re-run the formula and refresh the cached value


a = Signal(1)  # => source signal a
b = Signal(2)  # => source signal b
c = Computed(lambda: a.get() + b.get(), a, b)  # => c = a + b, kept up to date automatically

print(c.value)  # => 1 + 2, computed at construction time
# => Output: 3
a.set(10)  # => changing a automatically triggers c's recompute -- no manual "update c" call needed
print(c.value)  # => 10 + 2
# => Output: 12
b.set(20)  # => changing b ALSO automatically triggers c's recompute
print(c.value)  # => 10 + 20
# => Output: 30

"""Example 42: Reactive vs Manual Recompute."""

from collections.abc import Callable  # => types every no-argument callback stored below


class ManualPair:  # => BEFORE: caller must REMEMBER to update the derived value by hand
    def __init__(self, a: int, b: int) -> None:  # => constructor seeds both inputs and the derived total
        self.a = a  # => plain field, no notification wiring at all
        self.b = b  # => plain field, no notification wiring at all
        self.total = a + b  # => computed once -- nothing keeps this in sync automatically

    def set_a(self, value: int) -> None:  # => updates a but does NOT touch total -- easy to forget
        self.a = value  # => total is now STALE until someone remembers to call recompute_total()

    def recompute_total(self) -> None:  # => the easy-to-forget manual step
        self.total = self.a + self.b  # => must be called explicitly -- nothing calls it automatically


class Signal:  # => AFTER: the same minimal reactive primitive as example 41
    def __init__(self, initial: int) -> None:  # => constructor seeds the starting value
        self._value = initial  # => the current value, hidden behind get()/set() below
        self._on_change: list[Callable[[], None]] = []  # => callbacks to run whenever this signal changes

    def get(self) -> int:  # => read the current value
        return self._value  # => a plain read -- getting never triggers propagation

    def set(self, value: int) -> None:  # => setting AUTOMATICALLY notifies every dependent
        self._value = value  # => update the internal box first
        for callback in self._on_change:  # => automatically notify -- no dependent has to poll
            callback()  # => runs the dependent's recompute hook synchronously, right here

    def on_change(self, callback: Callable[[], None]) -> None:  # => register a dependent's recompute hook
        self._on_change.append(callback)  # => append only -- does NOT call callback with the current value


class ReactivePair:  # => wires a and b so total NEVER goes stale
    def __init__(self, a: int, b: int) -> None:  # => constructor wraps both inputs as Signals
        self.a = Signal(a)  # => a is now reactive, not a plain field
        self.b = Signal(b)  # => b is now reactive, not a plain field
        self.total = self.a.get() + self.b.get()  # => initial value
        self.a.on_change(self._recompute)  # => subscribe -- total tracks a automatically
        self.b.on_change(self._recompute)  # => subscribe -- total tracks b automatically

    def _recompute(self) -> None:  # => runs automatically whenever a or b changes
        self.total = self.a.get() + self.b.get()  # => the SAME formula as ManualPair, but never forgotten


manual = ManualPair(1, 2)  # => BEFORE
manual.set_a(10)  # => forgot to call recompute_total() -- a realistic mistake
print(manual.total)  # => STALE: still reflects the OLD a, not the new one
# => Output: 3

reactive = ReactivePair(1, 2)  # => AFTER
reactive.a.set(10)  # => the equivalent update, via the reactive API
print(reactive.total)  # => automatically current: 10 + 2
# => Output: 12

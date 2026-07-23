"""Example 56: Reactive Debounce."""

from collections.abc import Callable  # => types every downstream subscriber callback stored below


class DebouncedStream:  # => a stream operator: collapses a burst of pushes into just the LAST value
    def __init__(self) -> None:  # => constructor starts with no pending value and no subscribers
        self._pending: int | None = None  # => the most recent value pushed during the current burst
        self._downstream: list[Callable[[int], None]] = []  # => subscribers who only want the final value

    def subscribe(self, fn: Callable[[int], None]) -> None:  # => register a downstream listener
        self._downstream.append(fn)  # => append only -- does NOT call fn with anything yet

    def push(self, value: int) -> None:  # => called for every value in a burst -- does NOT notify yet
        self._pending = value  # => overwrite: only the latest value survives a burst

    def flush(self) -> None:  # => simulates "the debounce timer fired" -- deliver the last pending value
        if self._pending is not None:  # => only deliver if something was actually pushed since last flush
            for fn in self._downstream:  # => notify every subscriber with the FINAL value only
                fn(self._pending)  # => intermediate values 1 and 2 are never delivered to anyone
            self._pending = None  # => reset for the next burst


delivered: list[int] = []  # => records what downstream actually received
stream = DebouncedStream()  # => construct
stream.subscribe(lambda v: delivered.append(v))  # => subscribe once

stream.push(1)  # => burst: three rapid pushes
stream.push(2)  # => intermediate values during a burst are NEVER delivered on their own
stream.push(3)  # => only the last one, 3, matters
print(delivered)  # => nothing delivered yet -- the burst hasn't been flushed
# => Output: []

stream.flush()  # => the debounce timer "fires" -- only the LAST pushed value (3) reaches downstream
print(delivered)  # => exactly one delivery, and it is the final value of the burst
# => Output: [3]

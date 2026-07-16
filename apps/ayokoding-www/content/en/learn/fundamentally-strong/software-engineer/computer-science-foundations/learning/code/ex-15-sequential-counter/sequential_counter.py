# learning/code/ex-15-sequential-counter/sequential_counter.py
"""Example 15: A Clocked Counter -- Sequential State Held Across Calls."""  # => co-08: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic


class ClockedCounter:  # => co-08: SEQUENTIAL -- unlike Example 14's half-adder, this circuit has MEMORY
    """A counter that increments by 1 on every `tick()` -- state persists between calls."""  # => co-08: documents ClockedCounter's contract -- no runtime output, just sets its __doc__

    def __init__(self, width_bits: int = 4) -> None:  # => co-08: a fixed-width register -- wraps at 2**width_bits
        self._width_bits = width_bits  # => co-08: how many bits of state this "flip-flop bank" holds
        self._state = 0  # => co-08: the register's current value -- this IS the "memory" combinational logic lacks
        self._modulus = 1 << width_bits  # => co-08: 16 for a 4-bit counter -- the wraparound point

    def tick(self) -> int:  # => co-08: one "clock edge" -- reads current state, computes next, STORES it, returns old
        """Advance the counter by one clock tick; returns the state BEFORE this tick."""  # => co-08: documents tick's contract -- no runtime output, just sets its __doc__
        before = self._state  # => co-08: the value this call reports -- captured before mutation
        self._state = (self._state + 1) % self._modulus  # => co-08: next-state logic, WRAPPING at the register width
        return before  # => co-08: sequential circuits report state, then transition -- order matters for testing


if __name__ == "__main__":  # => co-08: entry point -- this block runs only when the file executes directly, not on import
    counter = ClockedCounter(width_bits=4)  # => co-08: one persistent object -- its `_state` is the "clock memory"
    observed: list[int] = []  # => co-08: records each tick's return value, in call order
    for _ in range(6):  # => co-08: six clock edges -- enough to show persistence AND, later, wraparound
        observed.append(counter.tick())  # => co-08: each call sees the PREVIOUS call's stored state, not a fresh 0
    print(f"six ticks returned: {observed}")  # => co-08: expect [0, 1, 2, 3, 4, 5] -- strictly increasing
    assert observed == [0, 1, 2, 3, 4, 5], "state must persist and increment across calls"  # => co-08
    for _ in range(10):  # => co-08: drive the counter past its 16-value modulus to prove wraparound
        counter.tick()  # => co-08: 6 (already ticked) + 10 more = 16 total ticks -- lands exactly back at 0
    wrapped = counter.tick()  # => co-08: the 17th tick reports the state AFTER 16 ticks, i.e. wrapped to 0
    print(f"after 16 total ticks, state wrapped to: {wrapped}")  # => co-08: expect 0 -- 16 mod 16 == 0
    assert wrapped == 0, "a 4-bit counter must wrap back to 0 after 16 ticks"  # => co-08: modulus behavior holds
    print("State persists across calls and wraps correctly: True")  # => co-08: both properties verified
    # => co-08: every assert above is this script's own regression check -- a clean exit means the claim held for these inputs

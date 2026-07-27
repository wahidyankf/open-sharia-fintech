"""Example 42: Vector Clock Detects a Conflict."""  # => co-15: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from dataclasses import dataclass  # => co-15: a typed vector clock -- one counter per replica that touched this key
from enum import Enum, auto  # => co-15: the 3-way comparison result vector clocks can produce


class ClockOrder(Enum):  # => co-15: comparing two vector clocks yields ONE of these 3 outcomes, never a 4th
    BEFORE = auto()  # => this clock happened strictly BEFORE the other -- a causal ancestor
    AFTER = auto()  # => this clock happened strictly AFTER the other -- a causal descendant
    CONCURRENT = auto()  # => co-15: NEITHER dominates the other -- a genuine, unresolved conflict


@dataclass(frozen=True)  # => frozen -- a vector clock snapshot is a stated fact about causal history
class VectorClock:  # => co-15: one counter per replica -- e.g. {"replica-A": 2, "replica-B": 1}
    counters: dict[str, int]  # => co-15: replica name -> how many writes THAT replica has causally seen


def compare(a: VectorClock, b: VectorClock) -> ClockOrder:  # => co-15: the core vector-clock comparison algorithm
    """Compare two vector clocks, returning BEFORE, AFTER, or CONCURRENT."""  # => documents the contract, no runtime output
    replicas = set(a.counters) | set(b.counters)  # => co-15: every replica EITHER clock has ever counted
    a_le_b = all(a.counters.get(r, 0) <= b.counters.get(r, 0) for r in replicas)  # => co-15: a dominates b on NO dimension
    b_le_a = all(b.counters.get(r, 0) <= a.counters.get(r, 0) for r in replicas)  # => co-15: b dominates a on NO dimension
    if a_le_b and not b_le_a:  # => co-15: a is <= b on every dimension, strictly less on at least one -- a happened BEFORE b
        return ClockOrder.BEFORE
    if b_le_a and not a_le_b:  # => co-15: the mirror image -- a happened AFTER b
        return ClockOrder.AFTER
    if a_le_b and b_le_a:  # => co-15: identical on every dimension -- treated as BEFORE (no real conflict, same causal point)
        return ClockOrder.BEFORE
    return ClockOrder.CONCURRENT  # => co-15: NEITHER dominates -- a and b happened independently, a genuine conflict


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    # Replica A writes, then replica B writes WITHOUT having seen A's write -- a genuine concurrent edit.
    clock_from_a = VectorClock({"replica-A": 1, "replica-B": 0})  # => co-15: replica-A's own write, replica-B's counter still 0
    clock_from_b = VectorClock({"replica-A": 0, "replica-B": 1})  # => co-15: replica-B's own write, replica-A's counter still 0

    order = compare(clock_from_a, clock_from_b)  # => co-15: neither clock dominates -- A doesn't know about B, B doesn't know about A
    assert order == ClockOrder.CONCURRENT  # => co-15: correctly flagged as CONCURRENT -- a genuine, unresolved conflict
    print(f"clock_from_a vs clock_from_b: {order.name}")  # => Output: clock_from_a vs clock_from_b: CONCURRENT
    # => co-15: unlike Example 41's LWW, NOTHING was auto-resolved here -- the vector clock only
    # => DETECTS the conflict; an application-level merge function (or human) must still decide
    # => the winner, or merge both values

    # A causally-ordered pair, for contrast: replica-A writes, then replica-A writes AGAIN, incrementing its own counter.
    clock_second_from_a = VectorClock({"replica-A": 2, "replica-B": 0})  # => co-15: strictly ahead of clock_from_a on replica-A's own counter
    order2 = compare(clock_from_a, clock_second_from_a)  # => co-15: clock_from_a is causally BEFORE clock_second_from_a
    assert order2 == ClockOrder.BEFORE  # => co-15: a genuinely ordered pair, correctly NOT flagged as a conflict
    print(f"clock_from_a vs clock_second_from_a: {order2.name}")  # => Output: clock_from_a vs clock_second_from_a: BEFORE


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script

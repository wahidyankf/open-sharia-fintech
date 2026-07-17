"""Example 41: pytest verification for Reactive Derived Value."""

from example import Computed, Signal


def test_computed_value_after_two_updates() -> None:
    a = Signal(1)  # => fresh signals, isolated from the module-level demo
    b = Signal(2)
    c = Computed(lambda: a.get() + b.get(), a, b)
    assert c.value == 3  # => 1 + 2 at construction

    a.set(10)  # => update source a
    assert c.value == 12  # => c recomputed automatically: 10 + 2

    b.set(20)  # => update source b too
    assert c.value == 30  # => c recomputed again: 10 + 20


def test_computed_never_needs_a_manual_recompute_call() -> None:
    a = Signal(0)  # => a fresh independent pair of signals
    b = Signal(0)
    c = Computed(lambda: a.get() * b.get(), a, b)
    a.set(5)
    b.set(4)
    assert c.value == 20  # => 5 * 4, with no explicit `c.recompute()` call anywhere in this test


# => Run: pytest -- Output: 2 passed

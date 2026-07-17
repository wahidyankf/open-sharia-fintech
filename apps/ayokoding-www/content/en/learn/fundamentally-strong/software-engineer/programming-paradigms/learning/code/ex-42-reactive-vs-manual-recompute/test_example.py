"""Example 42: pytest verification for Reactive vs Manual Recompute."""

from example import ManualPair, ReactivePair


def test_manual_pair_goes_stale_if_recompute_is_forgotten() -> None:
    pair = ManualPair(1, 2)  # => fresh instance
    pair.set_a(10)  # => update a, but never call recompute_total()
    assert pair.total == 3  # => STILL the old total -- this is the bug the reactive version prevents


def test_manual_pair_is_correct_only_after_an_explicit_recompute() -> None:
    pair = ManualPair(1, 2)  # => fresh instance
    pair.set_a(10)  # => update a
    pair.recompute_total()  # => remember to call it this time
    assert pair.total == 12  # => now correct, but only because of the explicit call


def test_reactive_pair_is_always_consistent_automatically() -> None:
    pair = ReactivePair(1, 2)  # => fresh instance
    pair.a.set(10)  # => the same conceptual update, no manual recompute anywhere
    assert pair.total == 12  # => correct immediately -- reactive propagation is automatic


# => Run: pytest -- Output: 3 passed

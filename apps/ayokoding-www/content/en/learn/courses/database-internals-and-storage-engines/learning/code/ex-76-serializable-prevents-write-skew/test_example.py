"""Example 76: pytest verification for Serializable Isolation Preventing Write Skew."""

from example import serializable_run


def test_exactly_one_transaction_aborts_under_the_detected_cycle() -> None:
    state = {"alice": True, "bob": True}
    alice_committed, bob_committed = serializable_run(state)
    assert (
        alice_committed != bob_committed
    )  # => exactly one committed, the other aborted


def test_the_shared_invariant_survives_because_one_transaction_was_blocked() -> None:
    state = {"alice": True, "bob": True}
    serializable_run(state)
    assert state["alice"] or state["bob"]


# => Run: pytest -- Output: 2 passed

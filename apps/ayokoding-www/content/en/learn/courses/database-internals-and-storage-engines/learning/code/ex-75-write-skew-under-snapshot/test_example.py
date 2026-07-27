"""Example 75: pytest verification for Write Skew Under Snapshot Isolation."""

from example import constraint_holds, snapshot_transaction


def test_both_transactions_commit_under_snapshot_isolation() -> None:
    state = {"a": True, "b": True}
    a_sees_b, b_sees_a = (
        state["b"],
        state["a"],
    )  # => both snapshots taken BEFORE either transaction runs
    committed_a = snapshot_transaction(state, "a", a_sees_b)
    committed_b = snapshot_transaction(state, "b", b_sees_a)
    assert committed_a and committed_b


def test_the_shared_constraint_ends_up_violated() -> None:
    state = {"a": True, "b": True}
    a_sees_b, b_sees_a = (
        state["b"],
        state["a"],
    )  # => both snapshots taken BEFORE either transaction runs
    snapshot_transaction(state, "a", a_sees_b)
    snapshot_transaction(state, "b", b_sees_a)
    assert not constraint_holds(state)


# => Run: pytest -- Output: 2 passed

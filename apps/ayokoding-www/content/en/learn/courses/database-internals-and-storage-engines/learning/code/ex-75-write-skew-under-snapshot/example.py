"""Example 75: Write Skew -- Permitted Under Snapshot Isolation."""
# Snapshot isolation (co-24, co-22) checks per-ROW conflicts only -- it misses cross-row constraints.

on_call: dict[str, bool] = {
    "alice": True,
    "bob": True,
}  # => the shared invariant: at least one True


def constraint_holds(
    state: dict[str, bool],
) -> bool:  # => the RULE both transactions rely on
    return any(
        state.values()
    )  # => at least one doctor must remain on call at all times


def snapshot_transaction(
    state: dict[str, bool], name: str, others_on_call: bool
) -> bool:  # => co-22 read/write
    if (
        others_on_call
    ):  # => this transaction's SNAPSHOT shows a colleague is still on call
        state[name] = (
            False  # => so it is "safe" (from this transaction's own snapshot's point of view)
        )
        return True  # => this transaction commits -- its snapshot never saw the other's concurrent change
    return False  # => would not have gone off call if the snapshot showed nobody else covering


alice_snapshot_sees_bob_on_call = on_call[
    "bob"
]  # => alice's transaction reads bob's state via its snapshot
bob_snapshot_sees_alice_on_call = on_call[
    "alice"
]  # => bob's transaction reads alice's state, SAME moment

alice_committed = snapshot_transaction(
    on_call, "alice", alice_snapshot_sees_bob_on_call
)  # => alice goes off
bob_committed = snapshot_transaction(
    on_call, "bob", bob_snapshot_sees_alice_on_call
)  # => bob ALSO goes off
print(alice_committed)  # => Output: True
print(bob_committed)  # => Output: True
print(on_call)  # => Output: {'alice': False, 'bob': False}

assert (
    alice_committed and bob_committed
)  # => snapshot isolation let BOTH transactions commit
assert not constraint_holds(
    on_call
)  # => yet the shared invariant is now VIOLATED -- this is write skew
print("ex-75 OK")  # => Output: ex-75 OK

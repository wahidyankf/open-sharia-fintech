"""Example 76: Serializable Isolation Prevents Write Skew."""
# Serializable isolation (co-24) detects the rw-antidependency CYCLE snapshot isolation ignores.


def serializable_run(
    state: dict[str, bool],
) -> tuple[bool, bool]:  # => co-24: SSI-style pair check
    alice_read_bob = state[
        "bob"
    ]  # => alice's snapshot read of bob, taken before either commits
    bob_read_alice = state[
        "alice"
    ]  # => bob's snapshot read of alice, taken at the SAME moment

    alice_committed = (
        alice_read_bob  # => alice only goes off-call if her snapshot showed bob on call
    )
    if (
        alice_committed
    ):  # => nothing conflicting has committed yet -- alice's commit is allowed
        state["alice"] = False  # => alice's write actually lands

    dangerous_cycle = (
        alice_committed and bob_read_alice
    )  # => the rw-antidependency SSI is built to catch
    bob_committed = (
        bob_read_alice and not dangerous_cycle
    )  # => bob is the one chosen to abort, not both
    if (
        bob_committed
    ):  # => only reached if no dangerous cycle was detected against alice's commit
        state["bob"] = (
            False  # => bob's write would land, but only in the no-conflict case
        )
    return (
        alice_committed,
        bob_committed,
    )  # => exactly one of the pair aborts when a cycle IS detected


on_call: dict[str, bool] = {
    "alice": True,
    "bob": True,
}  # => the same shared invariant as ex-75
alice_committed, bob_committed = serializable_run(
    on_call
)  # => run BOTH transactions through the SSI check
print(alice_committed)  # => Output: True
print(bob_committed)  # => Output: False
print(on_call)  # => Output: {'alice': False, 'bob': True}

assert (
    alice_committed and not bob_committed
)  # => bob is the ONE transaction SSI aborts, not both
assert (
    on_call["alice"] or on_call["bob"]
)  # => the shared invariant survives -- bob stayed on call
print("ex-76 OK")  # => Output: ex-76 OK

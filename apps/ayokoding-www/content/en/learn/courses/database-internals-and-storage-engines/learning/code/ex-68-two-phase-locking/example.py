"""Example 68: Two-Phase Locking -- Growing and Shrinking Phases."""
# 2PL (co-25) forbids acquiring ANY lock once a transaction has released its first one.


class TwoPhaseLockError(
    Exception
):  # => raised when a transaction violates the growing/shrinking split
    """Raised when a lock is acquired after the shrinking phase has begun."""  # => documents intent


class Transaction:  # => tracks one transaction's own lock-acquisition and lock-release history
    def __init__(self) -> None:  # => starts in the growing phase, holding nothing
        self.held: set[str] = set()  # => locks currently held by this transaction
        self.has_released: bool = (
            False  # => flips True the moment the FIRST lock is ever released
        )

    def acquire(self, resource: str) -> None:  # => the growing-phase-only operation
        if (
            self.has_released
        ):  # => shrinking phase already began -- 2PL forbids acquiring now
            raise TwoPhaseLockError(
                f"cannot acquire {resource!r} after the shrinking phase began"
            )  # => the violation
        self.held.add(resource)  # => a new lock, added while still in the growing phase

    def release(
        self, resource: str
    ) -> None:  # => the operation that FLIPS the transaction into shrinking
        self.held.discard(resource)  # => the lock is given up
        self.has_released = (
            True  # => from this point on, acquire() is permanently forbidden
        )


txn = Transaction()  # => a fresh transaction, still in its growing phase
txn.acquire("row-1")  # => growing phase -- allowed
txn.acquire("row-2")  # => growing phase -- still allowed
txn.release("row-1")  # => the FIRST release -- shrinking phase begins from here on

violated = False  # => flips to True only if the protocol is actually violated below
try:  # => attempt the forbidden acquire
    txn.acquire("row-3")  # => forbidden -- this is now the shrinking phase
except TwoPhaseLockError:  # => the exact violation 2PL is designed to prevent
    violated = True  # => confirms the guard actually fired
print(violated)  # => Output: True

assert violated  # => the attempted acquire-after-release was correctly rejected
assert "row-3" not in txn.held  # => the forbidden acquire never actually took effect
print("ex-68 OK")  # => Output: ex-68 OK

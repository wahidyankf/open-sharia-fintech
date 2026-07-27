"""Example 69: Strict 2PL Prevents Cascading Aborts."""
# Strict 2PL (co-25) holds WRITE locks until commit -- no one else can ever see an uncommitted write.


class LockConflictError(
    Exception
):  # => raised when a transaction wants a lock someone else still holds
    """Raised when a requested lock conflicts with a lock already held by another transaction."""  # => docstring


class StrictTwoPhaseLockManager:  # => write locks are held until an explicit commit() call
    def __init__(self) -> None:  # => starts with nothing locked by anyone
        self.write_locks: dict[
            str, int
        ] = {}  # => resource -> the txn_id currently holding its write lock

    def acquire_write(
        self, resource: str, txn_id: int
    ) -> None:  # => the growing-phase write-lock request
        holder = self.write_locks.get(
            resource
        )  # => who (if anyone) already holds this write lock
        if (
            holder is not None and holder != txn_id
        ):  # => someone ELSE holds it -- must wait, not proceed
            raise LockConflictError(
                f"{resource!r} is write-locked by txn {holder}, not txn {txn_id}"
            )  # => the block
        self.write_locks[resource] = (
            txn_id  # => granted (or re-confirmed for the same transaction)
        )

    def commit(
        self, txn_id: int
    ) -> None:  # => strict 2PL: ONLY commit releases this transaction's write locks
        held = [
            r for r, holder in self.write_locks.items() if holder == txn_id
        ]  # => everything txn_id holds
        for (
            resource
        ) in held:  # => release every write lock this transaction was holding
            del self.write_locks[
                resource
            ]  # => now available for another transaction to acquire


manager = StrictTwoPhaseLockManager()  # => a fresh lock manager, nothing locked yet
manager.acquire_write(
    "row-1", txn_id=1
)  # => txn 1 writes row-1, holding the lock (uncommitted so far)

blocked = (
    False  # => flips to True only if txn 2's conflicting request is actually rejected
)
try:  # => attempt the forbidden concurrent acquire
    manager.acquire_write(
        "row-1", txn_id=2
    )  # => txn 2 tries to read/write the SAME uncommitted row
except LockConflictError:  # => strict 2PL's guarantee firing exactly as designed
    blocked = True  # => confirms the guard actually fired
print(blocked)  # => Output: True

manager.commit(txn_id=1)  # => txn 1 finally commits, releasing its write lock
manager.acquire_write(
    "row-1", txn_id=2
)  # => NOW txn 2 can safely acquire it -- no dirty read ever happened

assert blocked  # => txn 2 was correctly blocked from touching txn 1's uncommitted write
print("ex-69 OK")  # => Output: ex-69 OK

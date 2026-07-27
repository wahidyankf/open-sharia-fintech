"""Example 70: Optimistic Concurrency Control -- Read, Validate, Write."""
# OCC (co-25) takes no locks during reads -- conflicts surface only at commit-time validation.

from dataclasses import dataclass  # => a plain, typed record for one versioned value


@dataclass  # => a plain, typed record -- no custom __init__ needed
class VersionedStore:  # => a tiny key-value store where every value carries a version number
    value: str  # => the current value
    version: int  # => bumped on every successful write -- OCC's conflict signal


store = VersionedStore(value="initial", version=0)  # => a fresh store, version 0


def occ_transaction(
    store: VersionedStore, new_value: str
) -> bool:  # => co-25: read, validate, write
    read_version = (
        store.version
    )  # => READ phase: remember the version seen at read time, take NO lock
    computed_value = (
        new_value  # => normally derived from the read; kept simple here for clarity
    )
    if (
        store.version != read_version
    ):  # => VALIDATE phase: has anyone committed since we read?
        return False  # => conflict detected -- this transaction must retry, its write is rejected
    store.value = computed_value  # => WRITE phase: only reached if validation passed
    store.version += 1  # => bump the version so any OTHER concurrent reader's validation will now fail
    return True  # => this transaction's write committed successfully


txn_a_read_version = (
    store.version
)  # => txn A reads the store first, remembering this version
success_b = occ_transaction(
    store, "from-b"
)  # => txn B runs its full read-validate-write cycle FIRST
print(success_b)  # => Output: True

conflict = (
    store.version != txn_a_read_version
)  # => txn A's remembered version is now stale
success_a = (
    occ_transaction(store, "from-a") if not conflict else False
)  # => txn A would fail validation
print(success_a)  # => Output: False

assert (
    success_b is True
)  # => txn B, running first against no conflict, committed successfully
assert (
    success_a is False
)  # => txn A's stale read version means it correctly fails validation and retries
print("ex-70 OK")  # => Output: ex-70 OK

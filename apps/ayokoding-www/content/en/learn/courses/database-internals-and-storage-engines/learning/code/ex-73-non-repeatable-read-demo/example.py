"""Example 73: Non-Repeatable Read -- Unstable Under Read-Committed, Stable Under Repeatable-Read."""
# Read-committed re-reads live data (co-24) -- repeatable-read fixes a snapshot for the WHOLE transaction.

committed_value = (
    "original"  # => the row's currently committed value, module-level for simplicity
)


def read_committed_fetch() -> (
    str
):  # => co-24: always returns whatever is committed RIGHT NOW
    return (
        committed_value  # => no memory of any earlier read within the same transaction
    )


def repeatable_read_fetch(
    snapshot_value: str,
) -> str:  # => co-24: always returns the FIXED snapshot value
    return (
        snapshot_value  # => ignores whatever has committed since the snapshot was taken
    )


first_read_committed = (
    read_committed_fetch()
)  # => a read-committed transaction's FIRST read
snapshot = (
    read_committed_fetch()
)  # => a repeatable-read transaction's snapshot, taken at the same moment

committed_value = "updated-by-someone-else"  # => a CONCURRENT transaction commits an update in between

second_read_committed = (
    read_committed_fetch()
)  # => the SAME read-committed transaction's SECOND read
second_read_repeatable = repeatable_read_fetch(
    snapshot
)  # => the repeatable-read transaction's second read
print(first_read_committed == second_read_committed)  # => Output: False
print(snapshot == second_read_repeatable)  # => Output: True

assert (
    first_read_committed != second_read_committed
)  # => the anomaly: read-committed's value CHANGED
assert (
    snapshot == second_read_repeatable
)  # => repeatable-read stayed stable across the concurrent commit
print("ex-73 OK")  # => Output: ex-73 OK

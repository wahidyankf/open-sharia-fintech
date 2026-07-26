"""Example 72: Dirty Read -- Present Under Read-Uncommitted, Gone Under Read-Committed."""
# A dirty read (co-24) exposes an UNCOMMITTED write -- read-committed specifically forbids this.

from dataclasses import (
    dataclass,
)  # => a plain, typed record for a row's committed vs pending state


@dataclass  # => a plain, typed record -- no custom __init__ needed
class Row:  # => models a row with a durable committed value and a separate, still-pending write
    committed_value: str  # => the last value some transaction actually committed
    pending_value: str | None = (
        None  # => an in-flight write, not yet committed by its own transaction
    )


def read_uncommitted(
    row: Row,
) -> str:  # => co-24: sees a pending write even before it commits
    return (
        row.pending_value if row.pending_value is not None else row.committed_value
    )  # => dirty read allowed


def read_committed(
    row: Row,
) -> str:  # => co-24: NEVER sees an uncommitted value, no matter what
    return (
        row.committed_value
    )  # => always the last COMMITTED value -- pending writes stay invisible


row = Row(
    committed_value="original"
)  # => nothing pending yet -- both levels would agree right now
row.pending_value = (
    "uncommitted-write"  # => a concurrent transaction has written but NOT committed
)

seen_under_uncommitted = read_uncommitted(
    row
)  # => what a read-uncommitted reader sees right now
seen_under_committed = read_committed(
    row
)  # => what a read-committed reader sees at the SAME moment
print(seen_under_uncommitted)  # => Output: uncommitted-write
print(seen_under_committed)  # => Output: original

assert (
    seen_under_uncommitted == "uncommitted-write"
)  # => the dirty-read anomaly appears here
assert (
    seen_under_committed == "original"
)  # => read-committed correctly hides the uncommitted write
print("ex-72 OK")  # => Output: ex-72 OK

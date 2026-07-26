"""Example 74: Phantom Read -- a New Row Appears Under (Lock-Based) Repeatable-Read."""
# Row-level locks (co-24) protect rows a query ALREADY matched, but not new rows inserted into a range.
# NOTE: this models the classic ANSI-SQL lock-based repeatable-read; real PostgreSQL REPEATABLE READ
# uses snapshot isolation instead (see ex-75), which closes this specific gap but permits write skew.

from dataclasses import dataclass  # => a plain, typed record for one table row


@dataclass
class Row:  # => a minimal row -- just enough to demonstrate the phantom
    id: int  # => the row's identity
    status: str  # => the column the range query filters on


table: list[Row] = [
    Row(id=1, status="active"),  # => matches the range query below
    Row(id=2, status="active"),  # => also matches the range query below
]  # => end of the table fixture


def range_query(
    status: str,
) -> list[Row]:  # => co-24: re-run twice within one transaction
    return [
        row for row in table if row.status == status
    ]  # => a fresh scan every time it is called


first_scan = range_query(
    "active"
)  # => the transaction's FIRST range read -- locks these two rows
first_ids = {
    row.id for row in first_scan
}  # => the row ids the first scan actually matched
print(sorted(first_ids))  # => Output: [1, 2]

table.append(
    Row(id=3, status="active")
)  # => a CONCURRENT transaction inserts a brand-new matching row
# => row-level locking never touched row 3 -- it didn't exist to lock when the first scan ran

second_scan = range_query(
    "active"
)  # => the SAME transaction's SECOND range read, same predicate
second_ids = {row.id for row in second_scan}  # => now includes the phantom
print(sorted(second_ids))  # => Output: [1, 2, 3]

assert first_ids == {
    1,
    2,
}  # => the first scan saw exactly the two originally matching rows
assert second_ids == {
    1,
    2,
    3,
}  # => the second scan sees a PHANTOM row that did not exist before
assert second_ids - first_ids == {3}  # => row 3 is precisely the phantom that appeared
print("ex-74 OK")  # => Output: ex-74 OK

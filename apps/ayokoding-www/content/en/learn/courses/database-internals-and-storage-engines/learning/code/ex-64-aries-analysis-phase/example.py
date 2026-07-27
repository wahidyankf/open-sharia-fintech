"""Example 64: ARIES Analysis Phase Reconstructs the Transaction and Dirty-Page Tables."""
# The analysis phase (co-18) scans forward from the checkpoint to rebuild in-memory recovery state.

from dataclasses import dataclass  # => a plain, typed record for one log entry


@dataclass  # => a plain, typed record -- no custom __init__ needed
class LogRecord:  # => a simplified ARIES-style log record
    lsn: int  # => this record's own log sequence number
    txn_id: int  # => which transaction issued it
    kind: str  # => "begin", "update", "commit", or "abort"
    page_id: int | None = None  # => which page an "update" touched, if any


log: list[
    LogRecord
] = [  # => a tiny log spanning two transactions, one committed, one not
    LogRecord(lsn=1, txn_id=1, kind="begin"),  # => txn 1 starts
    LogRecord(lsn=2, txn_id=1, kind="update", page_id=10),  # => txn 1 dirties page 10
    LogRecord(lsn=3, txn_id=2, kind="begin"),  # => txn 2 starts
    LogRecord(
        lsn=4, txn_id=1, kind="commit"
    ),  # => txn 1 finishes -- no longer a "loser"
    LogRecord(
        lsn=5, txn_id=2, kind="update", page_id=20
    ),  # => txn 2 dirties page 20, never commits
]  # => end of the log fixture


def analysis(
    log: list[LogRecord],
) -> tuple[set[int], dict[int, int]]:  # => co-18: rebuild BOTH tables
    transaction_table: set[int] = (
        set()
    )  # => transactions still active (no commit/abort record seen)
    dirty_page_table: dict[
        int, int
    ] = {}  # => page_id -> the EARLIEST LSN that dirtied it, uncheckpointed
    for record in log:  # => a single forward pass from the checkpoint is enough
        if record.kind == "begin":  # => a new transaction enters the table
            transaction_table.add(
                record.txn_id
            )  # => tracked as active until proven otherwise
        elif record.kind in (
            "commit",
            "abort",
        ):  # => this transaction is no longer active
            transaction_table.discard(
                record.txn_id
            )  # => removed -- it finished, one way or another
        elif (
            record.kind == "update" and record.page_id is not None
        ):  # => a page was dirtied
            if (
                record.page_id not in dirty_page_table
            ):  # => only the FIRST dirtying LSN matters
                dirty_page_table[record.page_id] = (
                    record.lsn
                )  # => record the earliest LSN for this page
    return (
        transaction_table,
        dirty_page_table,
    )  # => the two tables analysis is responsible for rebuilding


transaction_table, dirty_page_table = analysis(
    log
)  # => run the analysis pass over the fixture log
print(transaction_table)  # => Output: {2}
print(dirty_page_table)  # => Output: {10: 2, 20: 5}

assert transaction_table == {
    2
}  # => only txn 2 is still active -- txn 1 already committed
assert dirty_page_table == {
    10: 2,
    20: 5,
}  # => both dirtied pages, tagged with their earliest dirtying LSN
print("ex-64 OK")  # => Output: ex-64 OK

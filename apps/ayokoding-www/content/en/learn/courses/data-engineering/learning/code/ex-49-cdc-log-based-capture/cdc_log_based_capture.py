"""Worked Example 49: CDC -- Log-Based Capture Sees Everything."""  # => co-20: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from dataclasses import dataclass  # => co-20: models one row in a transaction log -- Debezium's own log-based CDC source


@dataclass  # => co-20: a single change-log entry, in the exact shape a transaction log actually records
class ChangeLogEntry:  # => co-20: one entry -- an insert, update, or delete, all captured the SAME way
    operation: str  # => co-20: "insert", "update", or "delete" -- the transaction log records ALL three, unlike polling
    row_id: int  # => co-20: which row this change applies to
    value: str | None  # => co-20: the row's new value -- None for a delete, since there's no "new value" to record


TRANSACTION_LOG = [  # => co-20: exactly the SAME sequence of real-world changes ex-48's polling missed most of
    ChangeLogEntry("insert", 1, "alice"),  # => co-20: row 1 created
    ChangeLogEntry("insert", 2, "bob"),  # => co-20: row 2 created
    ChangeLogEntry("insert", 3, "carol"),  # => co-20: row 3 created
    ChangeLogEntry("update", 2, "bob-updated"),  # => co-20: row 2 updated -- polling COULD have seen the final value, log-based sees the STEP too
    ChangeLogEntry("delete", 2, None),  # => co-20: row 2 deleted -- polling structurally CANNOT see this at all
    ChangeLogEntry("delete", 3, None),  # => co-20: row 3 deleted -- also invisible to polling
    ChangeLogEntry("insert", 4, "dave"),  # => co-20: row 4 created
]  # => co-20: closes TRANSACTION_LOG -- every operation type is present, in the order they actually happened

if __name__ == "__main__":  # => co-20: entry point -- runs only when this file executes directly, not on import
    operations_seen = [entry.operation for entry in TRANSACTION_LOG]  # => co-20: EVERY operation type this log actually recorded
    print(f"Operations captured by the transaction log, in order: {operations_seen}")  # => co-20: prints the full, ordered operation sequence

    insert_count = operations_seen.count("insert")  # => co-20: how many inserts were captured
    update_count = operations_seen.count("update")  # => co-20: how many updates were captured
    delete_count = operations_seen.count("delete")  # => co-20: how many deletes were captured -- THIS is what ex-48's polling missed
    print(f"Inserts: {insert_count} | Updates: {update_count} | Deletes: {delete_count}")  # => co-20: prints the operation-type breakdown
    assert insert_count == 4 and update_count == 1 and delete_count == 2, "all three operation types must be captured, correctly counted"  # => co-20

    all_three_types_present = {"insert", "update", "delete"}.issubset(set(operations_seen))  # => co-20: the claim ex-49 makes
    print(f"All three operation types (insert, update, delete) present: {all_three_types_present}")  # => co-20: prints the coverage check
    assert all_three_types_present, "log-based CDC must capture insert, update, AND delete -- unlike query-based polling"  # => co-20
    print(f"MATCH: {len(TRANSACTION_LOG)} log entries capture every operation type, including both deletes polling missed")  # => co-20
    # => co-20: log-based CDC reads the transaction log itself -- it sees every state TRANSITION, not just the current snapshot

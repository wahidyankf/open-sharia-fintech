"""Worked Example 48: CDC -- Query-Based Polling Misses Deletes."""  # => co-20: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def poll_for_changes(current_table: dict[int, str], *, last_seen_ids: set[int]) -> list[int]:  # => co-20: query-based CDC -- polls the CURRENT table state only
    """Return every row id present in current_table that wasn't in last_seen_ids -- a naive polling CDC."""  # => co-20: documents poll_for_changes's contract -- no runtime output, just sets its __doc__
    return [row_id for row_id in current_table if row_id not in last_seen_ids]  # => co-20: can only see what's THERE NOW -- nothing about what's GONE


if __name__ == "__main__":  # => co-20: entry point -- runs only when this file executes directly, not on import
    table_before = {1: "alice", 2: "bob", 3: "carol"}  # => co-20: the table's state at the LAST poll -- three rows
    last_seen_ids = set(table_before.keys())  # => co-20: what the poller already knew about, as of last time

    table_after = {1: "alice", 4: "dave"}  # => co-20: between polls: row 2 UPDATED then DELETED, row 3 DELETED, row 4 INSERTED
    new_ids = poll_for_changes(table_after, last_seen_ids=last_seen_ids)  # => co-20: what THIS poll can see as "new"
    print(f"Poll detects new ids: {new_ids}")  # => co-20: prints only what polling CAN see -- the insert

    deleted_ids = last_seen_ids - set(table_after.keys())  # => co-20: what ACTUALLY happened between polls (ground truth, not what polling sees)
    print(f"Rows that were actually deleted between polls: {sorted(deleted_ids)}")  # => co-20: ground truth -- rows 2 and 3 are GONE
    poll_detected_deletes = poll_for_changes(table_after, last_seen_ids=last_seen_ids)  # => co-20: does the SAME polling mechanism see any delete?
    detected_any_delete = any(row_id in deleted_ids for row_id in poll_detected_deletes)  # => co-20: does the "new ids" list mention a delete at all?
    print(f"Polling's own 'new ids' output mentions any deleted row: {detected_any_delete}")  # => co-20: prints the miss

    assert new_ids == [4], "polling can only report the genuinely NEW row -- id 4"  # => co-20: sanity check
    assert not detected_any_delete, "query-based polling, by construction, cannot report a delete at all"  # => co-20: the claim ex-48 makes
    print(f"MATCH: 2 rows were actually deleted (ids {sorted(deleted_ids)}), but polling's own output never mentions either one")  # => co-20
    # => co-20: query-based CDC can only see what's PRESENT right now -- it structurally cannot report a delete or a between-poll change

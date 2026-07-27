"""Example 34: pytest verification for WAL Undo Rolling Back Uncommitted Writes."""

from example import LogRecord, undo_losers


def test_uncommitted_write_is_rolled_back() -> None:
    log = [LogRecord(txn_id=1, key="k", before="old", after="new")]
    state = {"k": "new"}
    undo_losers(log, state, committed=set())
    assert state["k"] == "old"


def test_committed_write_is_left_alone() -> None:
    log = [LogRecord(txn_id=1, key="k", before="old", after="new")]
    state = {"k": "new"}
    undo_losers(log, state, committed={1})
    assert state["k"] == "new"  # => committed -- undo must never touch it


# => Run: pytest -- Output: 2 passed

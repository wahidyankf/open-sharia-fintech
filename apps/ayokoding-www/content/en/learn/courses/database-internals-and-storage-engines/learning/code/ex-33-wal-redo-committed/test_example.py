"""Example 33: pytest verification for WAL Redo Replaying Committed Writes."""

from example import LogRecord, redo_all


def test_committed_writes_survive_redo() -> None:
    log = [LogRecord(txn_id=1, key="k", value="v")]
    state = redo_all(log)
    assert state["k"] == "v"


def test_redo_replays_every_record_regardless_of_commit_status() -> None:
    log = [
        LogRecord(txn_id=1, key="k", value="v1"),
        LogRecord(txn_id=2, key="k", value="v2"),
    ]
    state = redo_all(log)
    assert state["k"] == "v2"  # => the LAST write in the log wins, whoever wrote it


# => Run: pytest -- Output: 2 passed

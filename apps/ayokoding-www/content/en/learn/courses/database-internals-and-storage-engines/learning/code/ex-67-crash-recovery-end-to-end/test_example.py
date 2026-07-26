"""Example 67: pytest verification for End-to-End Crash Recovery."""

from example import LogRecord, recover


def test_committed_transactions_survive_recovery() -> None:
    log = [
        LogRecord(lsn=1, txn_id=1, kind="begin"),
        LogRecord(lsn=2, txn_id=1, kind="update", key="x", before="old", after="new"),
        LogRecord(lsn=3, txn_id=1, kind="commit"),
    ]
    assert recover(log)["x"] == "new"


def test_uncommitted_transactions_are_undone_by_recovery() -> None:
    log = [
        LogRecord(lsn=1, txn_id=1, kind="begin"),
        LogRecord(lsn=2, txn_id=1, kind="update", key="x", before="old", after="new"),
    ]
    assert recover(log)["x"] == "old"


# => Run: pytest -- Output: 2 passed

"""Example 64: pytest verification for the ARIES Analysis Phase."""

from example import LogRecord, analysis


def test_only_uncommitted_transactions_remain_in_the_table() -> None:
    log = [
        LogRecord(lsn=1, txn_id=1, kind="begin"),
        LogRecord(lsn=2, txn_id=1, kind="commit"),
        LogRecord(lsn=3, txn_id=2, kind="begin"),
    ]
    transaction_table, _ = analysis(log)
    assert transaction_table == {2}


def test_dirty_page_table_keeps_the_earliest_lsn_per_page() -> None:
    log = [
        LogRecord(lsn=1, txn_id=1, kind="begin"),
        LogRecord(lsn=2, txn_id=1, kind="update", page_id=5),
        LogRecord(lsn=3, txn_id=1, kind="update", page_id=5),
    ]
    _, dirty_page_table = analysis(log)
    assert dirty_page_table == {5: 2}


# => Run: pytest -- Output: 2 passed

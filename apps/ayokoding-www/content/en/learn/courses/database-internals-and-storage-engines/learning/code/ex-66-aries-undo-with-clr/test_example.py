"""Example 66: pytest verification for ARIES Undo Writing Compensation Log Records."""

from example import LogRecord, undo_with_clr


def test_undo_writes_one_clr_per_loser_update() -> None:
    log = [LogRecord(lsn=1, txn_id=7, page_id=1, before="a")]
    clrs = undo_with_clr(log, loser_txn=7)
    assert len(clrs) == 1
    assert clrs[0].is_clr is True


def test_a_resumed_undo_does_not_redo_already_compensated_steps() -> None:
    log = [LogRecord(lsn=1, txn_id=7, page_id=1, before="a")]
    clrs = undo_with_clr(log, loser_txn=7)
    resumed = undo_with_clr(log + clrs, loser_txn=7)
    assert resumed == []


# => Run: pytest -- Output: 2 passed

"""Example 61: pytest verification for Group Commit Batching."""

from example import GroupCommitLog


def test_one_fsync_covers_the_whole_batch() -> None:
    log = GroupCommitLog()
    for txn_id in range(3):
        log.commit(txn_id)
    log.flush()
    assert log.fsync_count == 1


def test_every_batched_transaction_becomes_durable() -> None:
    log = GroupCommitLog()
    for txn_id in range(3):
        log.commit(txn_id)
    log.flush()
    assert log.durable == {0, 1, 2}


# => Run: pytest -- Output: 2 passed

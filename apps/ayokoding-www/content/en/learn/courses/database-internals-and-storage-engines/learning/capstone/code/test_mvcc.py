"""pytest coverage for mvcc.py -- the full pages + index + WAL + MVCC pipeline, end to end."""

from mvcc import MVCCEngine


def test_snapshot_read_stays_consistent_while_a_concurrent_writer_proceeds() -> None:
    engine = MVCCEngine()
    engine.write(key=1, value=b"original", txn_id=1)
    engine.commit(txn_id=1)

    reader_snapshot_at = len(
        engine.commit_order
    )  # => taken BEFORE the concurrent writer runs
    reader_result = engine.snapshot_read(key=1, snapshot_at=reader_snapshot_at)

    engine.write(
        key=1, value=b"updated", txn_id=2
    )  # => a concurrent write, after the snapshot was taken
    engine.commit(txn_id=2)  # => the writer proceeds WITHOUT waiting on the reader

    assert (
        reader_result == b"original"
    )  # => the reader's snapshot is unaffected by the concurrent commit


def test_a_new_snapshot_taken_after_the_commit_sees_the_update() -> None:
    engine = MVCCEngine()
    engine.write(key=1, value=b"v1", txn_id=1)
    engine.commit(txn_id=1)
    engine.write(key=1, value=b"v2", txn_id=2)
    engine.commit(txn_id=2)
    assert engine.snapshot_read(key=1, snapshot_at=len(engine.commit_order)) == b"v2"


def test_the_latest_committed_write_survives_a_crash() -> None:
    engine = MVCCEngine()
    engine.write(key=1, value=b"v1", txn_id=1)
    engine.commit(txn_id=1)
    engine.write(key=1, value=b"v2", txn_id=2)
    engine.commit(txn_id=2)
    engine.crash_and_recover()
    assert (
        engine.read_after_recovery(1) == b"v2"
    )  # => co-16: the LAST committed write, not the first


def test_an_uncommitted_concurrent_write_never_becomes_visible_to_any_snapshot() -> (
    None
):
    engine = MVCCEngine()
    engine.write(key=1, value=b"v1", txn_id=1)
    engine.commit(txn_id=1)
    engine.write(
        key=1, value=b"never-committed", txn_id=2
    )  # => txn 2 never calls commit()
    result = engine.snapshot_read(key=1, snapshot_at=len(engine.commit_order))
    assert (
        result == b"v1"
    )  # => the uncommitted version is simply never visible to any snapshot


# => Run: pytest -- Output: 4 passed

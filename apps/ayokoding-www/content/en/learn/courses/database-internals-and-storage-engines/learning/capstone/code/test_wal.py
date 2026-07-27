"""pytest coverage for wal.py -- write-ahead logging across a simulated crash."""

from wal import WriteAheadLog


def test_a_committed_write_is_readable_before_any_crash() -> None:
    wal = WriteAheadLog()
    wal.append(txn_id=1, key=1, value=b"v1")
    wal.commit(txn_id=1)
    assert wal.read(1) == b"v1"


def test_an_uncommitted_write_is_never_readable_even_before_a_crash() -> None:
    wal = WriteAheadLog()
    wal.append(txn_id=1, key=1, value=b"v1")  # => never committed
    assert wal.read(1) is None


def test_a_committed_write_survives_a_simulated_crash() -> None:
    wal = WriteAheadLog()
    wal.append(txn_id=1, key=1, value=b"v1")
    wal.commit(txn_id=1)
    wal.crash_and_recover()
    assert wal.read(1) == b"v1"


def test_an_uncommitted_write_does_not_survive_a_simulated_crash() -> None:
    wal = WriteAheadLog()
    wal.append(txn_id=1, key=1, value=b"v1")  # => never committed before the crash
    wal.crash_and_recover()
    assert wal.read(1) is None


def test_multiple_transactions_recover_independently() -> None:
    wal = WriteAheadLog()
    wal.append(txn_id=1, key=1, value=b"committed")
    wal.commit(txn_id=1)
    wal.append(txn_id=2, key=2, value=b"uncommitted")
    wal.crash_and_recover()
    assert wal.read(1) == b"committed"
    assert wal.read(2) is None


# => Run: pytest -- Output: 5 passed

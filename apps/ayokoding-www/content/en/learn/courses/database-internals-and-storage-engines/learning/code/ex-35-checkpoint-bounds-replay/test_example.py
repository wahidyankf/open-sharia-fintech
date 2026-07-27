"""Example 35: pytest verification for a Checkpoint Bounding Redo Replay."""

from example import LogRecord, redo_scan_range


def test_scan_starts_strictly_after_the_checkpoint() -> None:
    log = [LogRecord(1, "write"), LogRecord(2, "checkpoint"), LogRecord(3, "write")]
    assert redo_scan_range(log) == [3]


def test_no_checkpoint_means_scan_the_whole_log() -> None:
    log = [LogRecord(1, "write"), LogRecord(2, "write")]
    assert redo_scan_range(log) == [
        1,
        2,
    ]  # => nothing to skip -- no checkpoint exists yet


# => Run: pytest -- Output: 2 passed

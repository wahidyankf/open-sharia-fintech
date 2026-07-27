"""Example 65: pytest verification for ARIES Redo Repeating History."""

from example import LogRecord, redo_repeat_history


def test_redo_replays_the_uncommitted_writers_changes_too() -> None:
    log = [LogRecord(lsn=1, page_id=9, value="from-a-loser")]
    pages = redo_repeat_history(log)
    assert pages[9] == "from-a-loser"


def test_the_last_write_to_a_page_wins() -> None:
    log = [
        LogRecord(lsn=1, page_id=1, value="v1"),
        LogRecord(lsn=2, page_id=1, value="v2"),
    ]
    pages = redo_repeat_history(log)
    assert pages[1] == "v2"


# => Run: pytest -- Output: 2 passed

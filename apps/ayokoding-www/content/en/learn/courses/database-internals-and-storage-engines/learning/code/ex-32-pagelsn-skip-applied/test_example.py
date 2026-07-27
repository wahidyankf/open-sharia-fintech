"""Example 32: pytest verification for Skip Already-Applied Records via pageLSN."""

from example import LogRecord, redo


def test_records_at_or_below_pagelsn_are_skipped() -> None:
    log = [
        LogRecord(lsn=1, page_id=1, new_value="a"),
        LogRecord(lsn=2, page_id=1, new_value="b"),
    ]
    page_lsns = {1: 2}
    assert (
        redo(log, page_lsns) == {}
    )  # => both records were already reflected on the page


def test_records_above_pagelsn_are_reapplied() -> None:
    log = [
        LogRecord(lsn=1, page_id=1, new_value="a"),
        LogRecord(lsn=2, page_id=1, new_value="b"),
    ]
    page_lsns = {1: 0}
    assert redo(log, page_lsns) == {
        1: "b"
    }  # => the LAST record wins -- page ends at its final value


# => Run: pytest -- Output: 2 passed

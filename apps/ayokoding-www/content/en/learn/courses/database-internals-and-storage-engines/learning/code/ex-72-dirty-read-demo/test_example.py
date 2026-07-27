"""Example 72: pytest verification for the Dirty-Read Anomaly."""

from example import Row, read_committed, read_uncommitted


def test_read_uncommitted_exposes_the_pending_write() -> None:
    row = Row(committed_value="old", pending_value="dirty")
    assert read_uncommitted(row) == "dirty"


def test_read_committed_never_exposes_a_pending_write() -> None:
    row = Row(committed_value="old", pending_value="dirty")
    assert read_committed(row) == "old"


# => Run: pytest -- Output: 2 passed

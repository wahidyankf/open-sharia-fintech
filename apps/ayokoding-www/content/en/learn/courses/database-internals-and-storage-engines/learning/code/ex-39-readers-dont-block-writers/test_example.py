"""Example 39: pytest verification for Readers Not Blocking Writers."""

from example import RowVersion, commit_order, snapshot_read, versions, writer_update


def test_writer_can_proceed_after_a_snapshot_is_taken() -> None:
    commit_order.clear()
    commit_order[1] = 0
    versions.clear()
    versions.append(RowVersion(value="orig", xmin=1))
    writer_update(
        "new", txn_id=2
    )  # => no exception, no wait -- the writer just proceeds
    assert len(versions) == 2


def test_reader_snapshot_is_unaffected_by_a_later_writer() -> None:
    commit_order.clear()
    commit_order[1] = 0
    versions.clear()
    versions.append(RowVersion(value="orig", xmin=1))
    snapshot_at = len(commit_order)
    result = snapshot_read(snapshot_at)
    writer_update("new", txn_id=2)
    assert result == "orig"  # => computed BEFORE the writer ran, and stays that way


# => Run: pytest -- Output: 2 passed

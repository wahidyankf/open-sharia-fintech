"""Example 37: pytest verification for the Snapshot Visibility Rule."""

from example import RowVersion, commit, commit_order, is_visible


def test_snapshot_before_commit_cannot_see_it() -> None:
    commit_order.clear()
    commit(txn_id=9)
    version = RowVersion(value="v", xmin=9)
    assert is_visible(version, snapshot_at=0) is False


def test_snapshot_after_commit_can_see_it() -> None:
    commit_order.clear()
    commit(txn_id=9)
    version = RowVersion(value="v", xmin=9)
    assert is_visible(version, snapshot_at=1) is True


# => Run: pytest -- Output: 2 passed

"""Example 40: pytest verification for Vacuum Reclaiming Dead Versions."""

from example import RowVersion, commit_order, vacuum


def test_a_version_dead_before_every_active_snapshot_is_reclaimed() -> None:
    commit_order.clear()
    commit_order.update({1: 0, 2: 1})
    versions = [RowVersion(value="v1", xmin=1, xmax=2), RowVersion(value="v2", xmin=2)]
    survivors = vacuum(versions, oldest_active_snapshot=2)
    assert len(survivors) == 1


def test_a_version_needed_by_an_active_snapshot_is_kept() -> None:
    commit_order.clear()
    commit_order.update({1: 0, 2: 1})
    versions = [RowVersion(value="v1", xmin=1, xmax=2), RowVersion(value="v2", xmin=2)]
    survivors = vacuum(
        versions, oldest_active_snapshot=0
    )  # => a reader at position 0 still needs v1
    assert len(survivors) == 2


# => Run: pytest -- Output: 2 passed

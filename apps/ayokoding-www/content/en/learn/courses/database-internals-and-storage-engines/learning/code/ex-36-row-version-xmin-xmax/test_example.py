"""Example 36: pytest verification for Row Versions Tagged with xmin/xmax."""

from example import RowVersion, update


def test_update_sets_xmax_on_the_old_version() -> None:
    versions = [RowVersion(value="v1", xmin=1)]
    update(versions, new_value="v2", txn_id=5)
    assert versions[0].xmax == 5


def test_update_sets_xmin_on_the_new_version() -> None:
    versions = [RowVersion(value="v1", xmin=1)]
    update(versions, new_value="v2", txn_id=5)
    assert versions[1].xmin == 5
    assert versions[1].xmax is None  # => the newest version has no successor yet


# => Run: pytest -- Output: 2 passed

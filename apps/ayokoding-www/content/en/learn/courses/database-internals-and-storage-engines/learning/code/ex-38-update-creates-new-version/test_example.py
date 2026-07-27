"""Example 38: pytest verification for an Update Creating a New Version."""

from example import RowVersion, update


def test_update_appends_rather_than_overwrites() -> None:
    versions = [RowVersion(value="v1", xmin=1)]
    update(versions, new_value="v2", txn_id=2)
    assert len(versions) == 2
    assert versions[0].value == "v1"  # => the original object's value is untouched


def test_three_versions_are_three_distinct_objects() -> None:
    versions = [RowVersion(value="v1", xmin=1)]
    update(versions, new_value="v2", txn_id=2)
    update(versions, new_value="v3", txn_id=3)
    assert (
        len({id(v) for v in versions}) == 3
    )  # => three genuinely distinct objects, not aliases


# => Run: pytest -- Output: 2 passed

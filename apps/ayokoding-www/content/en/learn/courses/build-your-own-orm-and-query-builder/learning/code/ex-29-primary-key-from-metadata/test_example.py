"""Example 29: pytest verification for Primary Key From Metadata."""

from example import TableMeta, primary_key_of


def test_primary_key_read_explicitly_not_by_position() -> None:
    # => pk is registered FIRST here -- the opposite arrangement of the module example
    meta = TableMeta(name="tags", columns=("id", "label"), primary_key="id")
    assert primary_key_of(meta) == "id"  # => still correct regardless of column position


def test_two_tables_can_have_different_primary_keys() -> None:
    a = TableMeta(name="users", columns=("id", "email"), primary_key="id")
    b = TableMeta(name="settings", columns=("user_id", "key"), primary_key="user_id")
    assert primary_key_of(a) != primary_key_of(b)  # => each table's pk is independent metadata


# => Run: pytest -- Output: 2 passed

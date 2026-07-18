"""Example 32: pytest verification for Mapping Multiple Rows."""

from example import User, rows_to_users


def test_row_count_is_preserved() -> None:
    rows = [(1, "A"), (2, "B"), (3, "C"), (4, "D")]  # => four rows, none should be lost
    users = rows_to_users(rows)  # => maps all four in one call
    assert len(users) == 4  # => exact count preserved


def test_field_values_match_each_row_in_order() -> None:
    rows = [(10, "Xu"), (20, "Yara")]
    users = rows_to_users(rows)
    assert users[0] == User(id=10, name="Xu")  # => dataclass equality compares field values
    assert users[1] == User(id=20, name="Yara")  # => order preserved between input and output lists


# => Run: pytest -- Output: 2 passed

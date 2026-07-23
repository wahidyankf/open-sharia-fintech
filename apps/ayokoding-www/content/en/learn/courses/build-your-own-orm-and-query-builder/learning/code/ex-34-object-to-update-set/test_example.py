"""Example 34: pytest verification for Object to UPDATE SET Dict."""

from example import User, user_to_update_set


def test_primary_key_column_never_appears_in_set_dict() -> None:
    user = User(id=3, name="Xu", email="xu@example.com")  # => a fresh object
    set_values = user_to_update_set(user)  # => derives the SET dict
    assert "id" not in set_values  # => the one invariant this function guarantees


def test_set_dict_contains_every_other_column() -> None:
    user = User(id=1, name="Alice", email="alice@example.com")
    set_values = user_to_update_set(user)
    assert set_values == {"name": "Alice", "email": "alice@example.com"}  # => everything except the pk


# => Run: pytest -- Output: 2 passed

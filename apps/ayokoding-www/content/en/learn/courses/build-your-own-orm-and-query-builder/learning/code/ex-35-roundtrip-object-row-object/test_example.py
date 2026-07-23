"""Example 35: pytest verification for Object-Row-Object Round Trip."""

from example import User, row_to_user, user_to_row


def test_object_to_row_to_object_equals_original() -> None:
    original = User(id=42, name="Grace", email="grace@example.com")  # => the starting object
    row = user_to_row(original)  # => object -> row
    reloaded = row_to_user(row)  # => row -> object
    assert reloaded == original  # => no field drifted across the round trip
    assert reloaded is not original  # => equal VALUE, but a genuinely distinct object instance


def test_row_shape_matches_the_schema_column_order() -> None:
    user = User(id=1, name="Bob", email="bob@example.com")
    row = user_to_row(user)
    assert row == (1, "Bob", "bob@example.com")  # => (id, name, email), matching CREATE TABLE order


# => Run: pytest -- Output: 2 passed

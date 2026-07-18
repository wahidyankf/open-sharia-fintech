"""Example 33: pytest verification for Object to INSERT Values."""

from example import User, user_to_insert_values


def test_dict_has_exactly_the_objects_columns() -> None:
    user = User(id=9, name="Grace", email="grace@example.com")  # => a fresh object
    values = user_to_insert_values(user)  # => maps it to a column-to-value dict
    assert set(values.keys()) == {"id", "name", "email"}  # => matches the dataclass's own field set


def test_dict_values_match_the_objects_current_attributes() -> None:
    user = User(id=2, name="Bob", email="bob@example.com")
    values = user_to_insert_values(user)
    assert values["name"] == "Bob"  # => value read straight from the object, not from a stale copy
    assert values["id"] == 2  # => including the pk, ready for an INSERT (unlike Example 34's UPDATE dict)


# => Run: pytest -- Output: 2 passed

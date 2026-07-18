"""Example 30: pytest verification for Row Tuple to Object."""

from example import User, row_to_user


def test_tuple_columns_map_to_matching_attributes() -> None:
    user = row_to_user((7, "Grace", "grace@example.com"))  # => a fresh tuple, not from a live db
    assert (user.id, user.name, user.email) == (7, "Grace", "grace@example.com")  # => order preserved


def test_result_is_a_real_user_instance() -> None:
    user = row_to_user((1, "Alice", "alice@example.com"))
    assert isinstance(user, User)  # => not a tuple, not a dict -- a real typed object


# => Run: pytest -- Output: 2 passed

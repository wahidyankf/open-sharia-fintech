"""Example 31: pytest verification for Row Dict to Object."""

from example import User, row_to_user


def test_dict_keys_map_to_matching_attributes_regardless_of_order() -> None:
    # => keys deliberately out of "id, name, email" order in the dict literal
    row = {"name": "Grace", "email": "grace@example.com", "id": 7}
    user = row_to_user(row)  # => mapping reads by key, so dict insertion order is irrelevant
    assert isinstance(user, User)  # => a real typed User instance, not the raw dict
    assert (user.id, user.name, user.email) == (7, "Grace", "grace@example.com")  # => correct regardless


def test_missing_key_raises_key_error() -> None:
    incomplete_row = {"id": 1, "name": "Alice"}  # => "email" key deliberately missing
    try:
        row_to_user(incomplete_row)  # => must fail loudly, never silently default the field
        assert False, "expected KeyError"  # => this line must never execute
    except KeyError as exc:
        assert exc.args[0] == "email"  # => the missing key is named in the error


# => Run: pytest -- Output: 2 passed

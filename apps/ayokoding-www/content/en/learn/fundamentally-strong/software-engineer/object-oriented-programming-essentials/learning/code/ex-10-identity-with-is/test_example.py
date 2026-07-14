"""Example 10: pytest verification for Identity with is."""

from example import Dog


def test_aliased_name_is_identical_object() -> None:
    a: Dog = Dog("Rex")
    b: Dog = a  # => an alias, not a copy
    assert a is b  # => both names refer to the exact same object in memory


# => Run: pytest -- Output: 1 passed

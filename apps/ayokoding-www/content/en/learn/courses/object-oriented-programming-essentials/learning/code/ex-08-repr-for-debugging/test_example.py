"""Example 8: pytest verification for __repr__ for Debugging."""

from example import Dog


def test_repr_matches_expected_string() -> None:
    d: Dog = Dog("Rex")
    assert repr(d) == "Dog(name='Rex')"  # => the exact string __repr__ returns


# => Run: pytest -- Output: 1 passed

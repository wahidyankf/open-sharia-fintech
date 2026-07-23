"""Example 9: pytest verification for str vs. repr."""

from example import Dog


def test_str_and_repr_return_different_strings() -> None:
    d: Dog = Dog("Rex")
    assert str(d) != repr(d)  # => two distinct string forms exist for the same object
    assert str(d) == "a dog named Rex"
    assert repr(d) == "Dog(name='Rex')"


# => Run: pytest -- Output: 1 passed

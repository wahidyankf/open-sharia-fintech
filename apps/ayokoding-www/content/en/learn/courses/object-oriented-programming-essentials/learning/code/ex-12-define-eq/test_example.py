"""Example 12: pytest verification for Define __eq__ for Value Comparison."""

from example import Dog


def test_same_name_dogs_compare_equal() -> None:
    a: Dog = Dog("Rex")
    b: Dog = Dog("Rex")
    assert a == b  # => __eq__ now compares name, not object identity


def test_different_name_dogs_compare_unequal() -> None:
    assert Dog("Rex") != Dog("Fido")  # => different name values are never equal


# => Run: pytest -- Output: 2 passed

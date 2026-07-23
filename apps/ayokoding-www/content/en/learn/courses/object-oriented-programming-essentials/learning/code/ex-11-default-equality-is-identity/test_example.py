"""Example 11: pytest verification for Default Equality Falls Back to Identity."""

from example import Dog


def test_equal_looking_objects_compare_false_without_eq() -> None:
    a: Dog = Dog("Rex")
    b: Dog = Dog("Rex")  # => same name, but a DIFFERENT object
    assert (
        a != b
    )  # => default equality is identity: two distinct objects are never equal


# => Run: pytest -- Output: 1 passed

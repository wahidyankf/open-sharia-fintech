"""Example 1: pytest verification for Define a Minimal Class."""

from example import Dog  # => imports the class under test


def test_instance_type_matches_class() -> None:
    d: Dog = Dog()  # => constructs a fresh Dog instance
    assert type(d) is Dog  # => the built object's exact type is the Dog class itself


# => Run: pytest -- Output: 1 passed

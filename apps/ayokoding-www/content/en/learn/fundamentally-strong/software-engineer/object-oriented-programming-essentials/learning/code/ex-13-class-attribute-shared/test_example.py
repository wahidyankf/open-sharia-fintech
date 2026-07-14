"""Example 13: pytest verification for A Shared Class Attribute."""

from example import Dog


def test_instances_share_class_attribute() -> None:
    a: Dog = Dog("Rex")
    b: Dog = Dog("Fido")
    assert a.species == b.species == "canine"  # => both read the one class-level value


# => Run: pytest -- Output: 1 passed

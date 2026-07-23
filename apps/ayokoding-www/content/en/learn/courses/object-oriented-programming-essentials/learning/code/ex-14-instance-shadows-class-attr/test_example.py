"""Example 14: pytest verification for An Instance Attribute Shadows the Class Attribute."""

from example import Dog


def test_instance_assignment_shadows_only_that_instance() -> None:
    a: Dog = Dog("Rex")
    b: Dog = Dog("Fido")
    a.species = "wolf"  # => shadows Dog.species locally, on a only
    assert a.species == "wolf"
    assert b.species == "canine"  # => untouched: b never got its own instance attribute


# => Run: pytest -- Output: 1 passed

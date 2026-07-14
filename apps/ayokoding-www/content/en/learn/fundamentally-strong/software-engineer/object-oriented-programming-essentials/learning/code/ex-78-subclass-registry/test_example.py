"""Example 78: pytest verification for Auto-Registering Subclasses with __init_subclass__."""

from example import Circle, Shape, Square


def test_every_subclass_appears_in_the_registry_on_definition() -> None:
    assert (
        Shape.registry["Circle"] is Circle
    )  # => registered the moment the class was defined
    assert Shape.registry["Square"] is Square


# => Run: pytest -- Output: 1 passed

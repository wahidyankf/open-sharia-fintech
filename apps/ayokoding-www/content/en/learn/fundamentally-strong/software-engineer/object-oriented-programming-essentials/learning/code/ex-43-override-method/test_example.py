"""Example 43: pytest verification for Overriding a Method."""

from example import Animal, Cat


def test_subclass_override_replaces_base_behavior() -> None:
    assert Animal().speak() == "..."  # => the unmodified base behavior
    assert Cat().speak() == "Meow"  # => Cat's override runs instead of Animal's


# => Run: pytest -- Output: 1 passed

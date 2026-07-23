"""Example 45: pytest verification for Polymorphic Dispatch Over a Mixed List."""

from example import Animal, Cat, Dog


def test_each_element_dispatches_to_its_own_override() -> None:
    animals: list[Animal] = [Cat(), Dog(), Animal()]
    sounds: list[str] = [
        a.speak() for a in animals
    ]  # => one shared call-site, three behaviors
    assert sounds == ["Meow", "Woof", "..."]


# => Run: pytest -- Output: 1 passed

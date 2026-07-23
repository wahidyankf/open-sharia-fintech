"""Example 49: pytest verification for A classmethod Factory Returns the Subclass Type."""

from example import Animal, Cat


def test_classmethod_factory_returns_calling_subclass() -> None:
    assert type(Animal.create()) is Animal  # => called on Animal -- cls is Animal
    assert type(Cat.create()) is Cat  # => called on Cat -- cls is Cat, same method body


# => Run: pytest -- Output: 1 passed

"""Example 46: pytest verification for isinstance Across a Hierarchy."""

from example import Animal, Cat


def test_isinstance_holds_across_the_hierarchy() -> None:
    c: Cat = Cat()
    assert isinstance(c, Cat)  # => matches its own, exact class
    assert isinstance(c, Animal)  # => ALSO matches every ancestor class


# => Run: pytest -- Output: 1 passed

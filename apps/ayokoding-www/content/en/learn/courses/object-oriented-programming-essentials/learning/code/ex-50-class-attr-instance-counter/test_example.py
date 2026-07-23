"""Example 50: pytest verification for A Class-Attribute Instance Counter."""

from example import Dog


def test_population_counts_every_constructed_instance() -> None:
    before: int = (
        Dog.population
    )  # => baseline, in case another test constructed Dogs first
    Dog("Rex")
    Dog("Fido")
    Dog("Max")
    assert Dog.population == before + 3  # => exactly three more instances were created


# => Run: pytest -- Output: 1 passed

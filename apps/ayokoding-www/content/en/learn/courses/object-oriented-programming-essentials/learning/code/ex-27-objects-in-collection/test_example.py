"""Example 27: pytest verification for Objects in a Collection."""

from example import Dog


def test_iteration_yields_each_object_in_order() -> None:
    dogs: list[Dog] = [Dog("Rex"), Dog("Fido"), Dog("Max")]
    names: list[str] = [
        dog.name for dog in dogs
    ]  # => walks the list in construction order
    assert names == ["Rex", "Fido", "Max"]


# => Run: pytest -- Output: 1 passed

"""Example 63: pytest verification for An ABC Providing a Concrete Shared Helper."""

from example import Square


def test_subclass_inherits_shared_concrete_helper() -> None:
    assert (
        Square(3.0).describe() == "Square: area=9.00"
    )  # => inherited, not redefined, method


# => Run: pytest -- Output: 1 passed

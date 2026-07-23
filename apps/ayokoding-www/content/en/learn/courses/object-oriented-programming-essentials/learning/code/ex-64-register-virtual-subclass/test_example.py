"""Example 64: pytest verification for Registering a Virtual Subclass."""

from example import Shape, ThirdPartyCircle


def test_registered_class_passes_isinstance_without_inheriting() -> None:
    Shape.register(
        ThirdPartyCircle
    )  # => idempotent to call more than once across test runs
    assert isinstance(
        ThirdPartyCircle(1.0), Shape
    )  # => True with no `class ThirdPartyCircle(Shape)`


# => Run: pytest -- Output: 1 passed

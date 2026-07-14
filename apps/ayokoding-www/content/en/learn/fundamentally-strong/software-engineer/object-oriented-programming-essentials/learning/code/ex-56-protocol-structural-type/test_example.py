"""Example 56: pytest verification for typing.Protocol Formalizes Duck Typing."""

from example import Circle, HasArea


def test_class_satisfies_protocol_without_inheriting() -> None:
    circle: Circle = Circle(2.0)
    assert isinstance(
        circle, HasArea
    )  # => structural match, with no `class Circle(HasArea)` anywhere


def test_class_bases_do_not_mention_the_protocol() -> None:
    assert (
        HasArea not in Circle.__bases__
    )  # => confirms there is genuinely no inheritance link


# => Run: pytest -- Output: 2 passed

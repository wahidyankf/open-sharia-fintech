"""Example 66: pytest verification for Refactoring Stack to Composition."""

from example import Stack


def test_only_push_pop_peek_are_public() -> None:
    s: Stack = Stack()
    s.push(1)
    s.push(2)
    assert s.peek() == 2
    assert s.pop() == 2
    assert not hasattr(
        s, "insert"
    )  # => composition means Stack exposes only its OWN interface


def test_original_push_pop_behavior_still_holds() -> None:
    s: Stack = Stack()
    s.push(10)
    assert s.pop() == 10  # => the tests Example 65's Stack would also have passed


# => Run: pytest -- Output: 2 passed

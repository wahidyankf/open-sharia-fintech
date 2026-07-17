"""Example 77: pytest verification for the Potential-Method Multi-Pop Stack."""

from example import MultiPopStack, potential


def test_multipop_never_pops_more_than_the_stack_holds() -> None:
    stack = MultiPopStack()
    for value in range(5):
        stack.push(value)
    actual = stack.multipop(1_000)  # => k is FAR larger than the stack's 5 elements
    assert actual == 5  # => capped at the actual stack size, not the requested k
    assert stack.items == []


def test_partial_multipop_removes_exactly_k_elements() -> None:
    stack = MultiPopStack()
    for value in range(10):
        stack.push(value)
    actual = stack.multipop(4)  # => k SMALLER than the stack -- a normal partial pop
    assert actual == 4
    assert len(stack.items) == 6
    assert stack.items == [0, 1, 2, 3, 4, 5]  # => the 4 most-recently-pushed are gone


def test_potential_equals_current_stack_size() -> None:
    stack = MultiPopStack()
    assert potential(stack) == 0  # => an empty stack has zero potential
    stack.push(1)
    stack.push(2)
    assert potential(stack) == 2
    stack.multipop(1)
    assert potential(stack) == 1  # => potential tracks size exactly, after every op


# => Run: pytest -- Output: 3 passed

"""Example 65: pytest verification for A Naive Stack(list) Leaks the Wrong Interface."""

from example import Stack


def test_naive_stack_leaks_list_insert() -> None:
    s: Stack = Stack()
    s.push(1)
    s.push(2)
    s.insert(0, 99)  # => a method a stack should never have exposed
    assert list(s) == [
        99,
        1,
        2,
    ]  # => reproduces the interface leak: insert() bypassed push/pop


# => Run: pytest -- Output: 1 passed

"""Example 4: pytest verification for Tuple Immutability vs. List Mutability."""


def test_list_allows_item_assignment() -> None:
    items = [1, 2, 3]
    items[0] = 99  # => legal for a list
    assert items == [99, 2, 3]


def test_tuple_rejects_item_assignment() -> None:
    values = (1, 2, 3)
    try:
        values[0] = 99  # type: ignore[index]  # => tuples have no __setitem__
        raised = False
    except TypeError:
        raised = True
    assert raised is True  # => confirms immutability is actually enforced
    assert values == (1, 2, 3)  # => unchanged


# => Run: pytest -- Output: 2 passed

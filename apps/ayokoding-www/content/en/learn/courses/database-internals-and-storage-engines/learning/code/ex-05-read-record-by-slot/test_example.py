"""Example 5: pytest verification for Read a Record by Slot Index."""

from example import insert, new_page, read_by_slot


def test_each_slot_resolves_to_its_own_record() -> None:
    page = new_page()
    idx1 = insert(page, b"one")
    idx2 = insert(page, b"two-two")
    assert read_by_slot(page, idx1) == b"one"
    assert read_by_slot(page, idx2) == b"two-two"


def test_slot_indexes_are_sequential() -> None:
    page = new_page()
    indexes = [insert(page, str(i).encode()) for i in range(4)]
    assert indexes == [0, 1, 2, 3]  # => slot indexes assign in insertion order


# => Run: pytest -- Output: 2 passed

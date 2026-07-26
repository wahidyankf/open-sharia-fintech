"""Example 6: pytest verification for the Free-Space Guard."""

import pytest

from example import PageFullError, free_space, insert, new_page


def test_free_space_shrinks_after_insert() -> None:
    page = new_page()
    before = free_space(page)
    insert(page, b"x" * 100)
    assert (
        free_space(page) < before
    )  # => both the slot AND the record consumed free space


def test_insert_raises_when_free_space_is_insufficient() -> None:
    page = new_page()
    insert(page, b"x" * 4000)
    with pytest.raises(PageFullError):
        insert(
            page, b"y" * 200
        )  # => the remaining free space can't fit this record + its slot


# => Run: pytest -- Output: 2 passed

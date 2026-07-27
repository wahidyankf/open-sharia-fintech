"""Example 1: pytest verification for Fixed-Size Page Allocation."""

from example import PAGE_SIZE, new_page


def test_page_length_equals_page_size() -> None:
    page = new_page()  # => allocate via the SAME constructor example.py uses
    assert len(page) == PAGE_SIZE  # => every allocated page is exactly PAGE_SIZE bytes


def test_fresh_page_is_zero_filled() -> None:
    page = new_page()  # => a second, independent allocation
    assert page == bytearray(
        PAGE_SIZE
    )  # => no stale bytes leak in from a prior allocation


# => Run: pytest -- Output: 2 passed

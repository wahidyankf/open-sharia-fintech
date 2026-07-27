"""Example 10: pytest verification for Buffer Pool Page-Table Lookup."""

from example import Frame


def test_resident_lookup_returns_its_frame() -> None:
    page_table: dict[int, Frame] = {1: Frame(page_id=1, data=b"one")}
    assert page_table.get(1) is not None
    assert page_table[1].data == b"one"


def test_non_resident_lookup_returns_none() -> None:
    page_table: dict[int, Frame] = {1: Frame(page_id=1, data=b"one")}
    assert page_table.get(99) is None  # => no frame exists for page 99


# => Run: pytest -- Output: 2 passed

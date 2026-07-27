"""Example 4: pytest verification for Insert a Fixed-Size Record from the Back."""

from example import header, insert_record_from_back, new_page


def test_pd_upper_shrinks_by_record_length() -> None:
    page = new_page()
    _, before = header(page)
    insert_record_from_back(page, b"12345")
    _, after = header(page)
    assert after == before - 5  # => a 5-byte record shrinks pd_upper by exactly 5


def test_record_reads_back_unchanged() -> None:
    page = new_page()
    offset = insert_record_from_back(page, b"payload!")
    assert (
        page[offset : offset + len(b"payload!")] == b"payload!"
    )  # => bytes round-trip exactly


# => Run: pytest -- Output: 2 passed

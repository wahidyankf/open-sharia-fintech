"""Example 7: pytest verification for Variable-Length Records."""

from example import insert, new_page, read


def test_short_and_long_records_coexist() -> None:
    page = new_page()
    short_idx = insert(page, b"hi")
    long_idx = insert(page, b"a genuinely much longer row of bytes")
    assert read(page, short_idx) == b"hi"
    assert read(page, long_idx) == b"a genuinely much longer row of bytes"


def test_each_record_reads_at_its_own_length() -> None:
    page = new_page()
    idx = insert(page, b"12345")
    assert (
        len(read(page, idx)) == 5
    )  # => the slot's OWN length field governs, not a fixed stride


# => Run: pytest -- Output: 2 passed

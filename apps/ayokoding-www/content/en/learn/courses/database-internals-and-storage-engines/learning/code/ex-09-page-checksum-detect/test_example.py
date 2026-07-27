"""Example 9: pytest verification for Page Checksum Detection."""

from example import checksum


def test_identical_pages_checksum_identically() -> None:
    page = bytearray(4096)
    page[50:60] = b"same-bytes"
    assert checksum(bytes(page)) == checksum(
        bytes(page)
    )  # => deterministic: same bytes, same checksum


def test_single_bit_flip_changes_the_checksum() -> None:
    page = bytearray(4096)
    page[50:60] = b"same-bytes"
    flipped = bytearray(page)
    flipped[0] ^= 0x01
    assert checksum(bytes(page)) != checksum(
        bytes(flipped)
    )  # => one bit is enough to detect corruption


# => Run: pytest -- Output: 2 passed

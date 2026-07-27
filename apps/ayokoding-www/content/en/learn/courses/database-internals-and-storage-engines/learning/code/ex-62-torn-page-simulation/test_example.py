"""Example 62: pytest verification for Torn-Page Detection via Checksum."""

from example import is_torn, make_page


def test_an_intact_page_is_never_flagged_as_torn() -> None:
    page = make_page(b"\x05")
    assert not is_torn(page)


def test_a_partially_overwritten_page_is_flagged_as_torn() -> None:
    old_page = make_page(b"\x01")
    new_page = make_page(b"\x02")
    torn = bytearray(old_page)
    torn[4:8] = new_page[4:8]
    assert is_torn(torn)


# => Run: pytest -- Output: 2 passed

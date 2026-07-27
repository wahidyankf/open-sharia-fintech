"""Example 63: pytest verification for Full-Page-Write Recovery."""

from example import checksum_of, log_full_page_if_first_write, repair_if_torn


def test_an_intact_page_is_returned_unchanged() -> None:
    body = b"\x09" * 16
    log_full_page_if_first_write(page_id=2, page_body=body)
    repaired = repair_if_torn(page_id=2, body=body, stored_checksum=checksum_of(body))
    assert repaired == body


def test_a_torn_page_is_replaced_by_the_logged_full_image() -> None:
    original = b"\x03" * 16
    log_full_page_if_first_write(page_id=3, page_body=original)
    torn = b"\xff" * 16
    repaired = repair_if_torn(
        page_id=3, body=torn, stored_checksum=checksum_of(original)
    )
    assert repaired == original


# => Run: pytest -- Output: 2 passed

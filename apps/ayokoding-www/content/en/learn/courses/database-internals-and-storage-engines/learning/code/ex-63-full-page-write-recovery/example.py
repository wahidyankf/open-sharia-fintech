"""Example 63: Full-Page-Write Recovery Repairs a Torn Page."""
# A full-page image logged on first write after checkpoint (co-26) can REPAIR a torn page on recovery.

import zlib  # => stdlib CRC32, standing in for a page checksum

full_page_log: dict[
    int, bytes
] = {}  # => page_id -> the FIRST full page image logged since the checkpoint


def log_full_page_if_first_write(
    page_id: int, page_body: bytes
) -> None:  # => only logs ONCE per checkpoint
    if (
        page_id not in full_page_log
    ):  # => this is the first write to this page since the last checkpoint
        full_page_log[page_id] = (
            page_body  # => log the ENTIRE page, not just the change -- the safety net
        )


def checksum_of(body: bytes) -> int:  # => a page's own integrity check
    return zlib.crc32(body)  # => any single-bit difference changes this value


def repair_if_torn(
    page_id: int, body: bytes, stored_checksum: int
) -> bytes:  # => co-26's recovery step
    if (
        checksum_of(body) == stored_checksum
    ):  # => the page is intact -- no repair needed
        return body  # => already correct -- nothing to repair
    return full_page_log[
        page_id
    ]  # => torn -- fall back to the logged full-page image, byte for byte


original_body = (
    b"\x01" * 16
)  # => the page's content immediately after the last checkpoint
log_full_page_if_first_write(
    page_id=1, page_body=original_body
)  # => logged BEFORE any change is applied
stored_checksum = checksum_of(
    original_body
)  # => the checksum that would have been written alongside it

torn_body = (
    b"\x02" * 8 + b"\x00" * 8
)  # => a crash left this page half-new, half-garbage -- torn
repaired = repair_if_torn(
    page_id=1, body=torn_body, stored_checksum=stored_checksum
)  # => run the repair
print(repaired == original_body)  # => Output: True

assert (
    repaired == original_body
)  # => the full-page image exactly repaired the torn page
print("ex-63 OK")  # => Output: ex-63 OK

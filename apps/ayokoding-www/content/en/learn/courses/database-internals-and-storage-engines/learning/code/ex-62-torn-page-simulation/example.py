"""Example 62: Torn-Page Simulation Detected by Checksum."""
# A page write is NOT atomic across a crash (co-26) -- a torn page mixes old and new bytes.

import zlib  # => stdlib CRC32, standing in for a page checksum

PAGE_SIZE = 16  # => a tiny illustrative page size, in bytes


def make_page(
    fill: bytes,
) -> bytearray:  # => a full page of one repeated fill byte, plus its checksum
    body = bytearray(fill * PAGE_SIZE)  # => the page's actual content
    checksum = zlib.crc32(bytes(body))  # => computed over the FULL, consistent page
    return (
        bytearray(checksum.to_bytes(4, "big")) + body
    )  # => checksum prefix + page body


def is_torn(
    page: bytearray,
) -> bool:  # => detects a torn write by recomputing the checksum
    stored_checksum = int.from_bytes(
        page[:4], "big"
    )  # => the checksum written when the page was whole
    body = bytes(page[4:])  # => the (possibly torn) body bytes as they exist NOW
    return (
        zlib.crc32(body) != stored_checksum
    )  # => mismatch means the bytes are inconsistent -- torn


old_page = make_page(
    b"\x01"
)  # => the fully-written OLD page, checksum matches its own body
new_page = make_page(
    b"\x02"
)  # => what the page SHOULD look like after a complete overwrite

torn_page = bytearray(old_page)  # => start from the old, consistent page
half = (
    4 + PAGE_SIZE // 2
)  # => the checksum prefix plus half the body -- where the "crash" interrupts
torn_page[4:half] = new_page[
    4:half
]  # => only the FIRST half was actually written before the crash
# => torn_page now holds: old checksum, new bytes for the first half, old bytes for the second half

print(is_torn(old_page))  # => Output: False
print(is_torn(torn_page))  # => Output: True

assert not is_torn(
    old_page
)  # => a page that was never partially overwritten is NOT torn
assert is_torn(
    torn_page
)  # => the half-old/half-new mix fails its own checksum -- correctly detected
print("ex-62 OK")  # => Output: ex-62 OK

"""Example 4: Insert a Fixed-Size Record from the Back of the Page."""

import struct  # => stdlib module for packing/unpacking fixed-layout binary fields

PAGE_SIZE: int = 4096  # => same 4 KB page size used throughout this course
HEADER_SIZE: int = 4  # => pd_lower(uint16) + pd_upper(uint16), same layout as Example 2


def new_page() -> (
    bytearray
):  # => allocates one empty page with a fresh header already packed in
    page = bytearray(PAGE_SIZE)  # => zero-filled buffer
    struct.pack_into(
        "<HH", page, 0, HEADER_SIZE, PAGE_SIZE
    )  # => empty page: no slots, no tuples yet
    return page  # => ready for inserts


def header(
    page: bytearray,
) -> tuple[int, int]:  # => reads the two header offsets back out
    lo, hi = struct.unpack_from("<HH", page, 0)  # => reads pd_lower, pd_upper in place
    return int(lo), int(hi)  # => plain Python ints, not struct's internal tuple type


def insert_record_from_back(
    page: bytearray, record: bytes
) -> int:  # => returns the record's new offset
    pd_lower, pd_upper = header(page)  # => unpack the header before writing anything
    new_upper = pd_upper - len(
        record
    )  # => tuple data grows DOWNWARD, so subtract to make room
    page[new_upper:pd_upper] = (
        record  # => the record's bytes land just before the OLD pd_upper
    )
    struct.pack_into(
        "<HH", page, 0, pd_lower, new_upper
    )  # => persist the lowered pd_upper
    return new_upper  # => also the record's own offset -- pd_upper only ever moves down


page: bytearray = new_page()  # => one fresh page
_, upper_before = header(page)  # => 4096: nothing stored yet
offset = insert_record_from_back(page, b"row-001")  # => a 7-byte record
_, upper_after = header(page)  # => re-read the header after the insert
print((upper_before, offset, upper_after))  # => Output: (4096, 4089, 4089)
# => notice offset == upper_after: the record IS the newly-reserved tail of the page

assert upper_after == upper_before - len(
    b"row-001"
)  # => pd_upper drops by exactly the record's size
assert (
    page[offset : offset + 7] == b"row-001"
)  # => the record's bytes are readable back at its offset
print("ex-04 OK")  # => Output: ex-04 OK

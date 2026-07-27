"""Example 7: Variable-Length Records Addressed by Slot."""

import struct  # => stdlib module for packing/unpacking fixed-layout binary fields

PAGE_SIZE: int = 4096  # => same 4 KB page size used throughout this course
HEADER_SIZE: int = 4  # => pd_lower(uint16) + pd_upper(uint16)
SLOT_SIZE: int = 4  # => offset(uint16) + length(uint16) per slot


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


def insert(
    page: bytearray, record: bytes
) -> int:  # => each call may store a DIFFERENT-length record
    pd_lower, pd_upper = header(page)  # => unpack the header before writing anything
    new_upper = pd_upper - len(
        record
    )  # => length varies per call -- no fixed record stride
    page[new_upper:pd_upper] = (
        record  # => write exactly len(record) bytes, whatever that length is
    )
    struct.pack_into(
        "<HH", page, pd_lower, new_upper, len(record)
    )  # => length travels WITH the slot
    struct.pack_into(
        "<HH", page, 0, pd_lower + SLOT_SIZE, new_upper
    )  # => persist the advanced header
    return (pd_lower - HEADER_SIZE) // SLOT_SIZE  # => this record's new slot index


def read(
    page: bytearray, slot_index: int
) -> bytes:  # => reads a record at whatever length ITS slot says
    slot_pos = (
        HEADER_SIZE + slot_index * SLOT_SIZE
    )  # => byte offset of this slot in the array
    off, length = struct.unpack_from(
        "<HH", page, slot_pos
    )  # => each slot's OWN length, not a global one
    return bytes(
        page[int(off) : int(off) + int(length)]
    )  # => slice out exactly `length` bytes


page: bytearray = new_page()  # => one fresh page to hold both records
short_idx = insert(page, b"hi")  # => a 2-byte record
long_idx = insert(page, b"a much longer variable-length row")  # => a 33-byte record
print(read(page, short_idx))  # => Output: b'hi'
print(read(page, long_idx))  # => Output: b'a much longer variable-length row'
# => two wildly different lengths, same page, same slot-based read function

assert (
    len(read(page, short_idx)) == 2
)  # => the short record reads back at its OWN length
assert (
    len(read(page, long_idx)) == 33
)  # => the long record reads back at ITS OWN length, unaffected
print("ex-07 OK")  # => Output: ex-07 OK

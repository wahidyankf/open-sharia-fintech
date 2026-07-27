"""Example 5: Read a Record by Slot Index -- the indirection that makes a slot a stable handle."""

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
) -> int:  # => inserts a record, returns its NEW SLOT INDEX
    pd_lower, pd_upper = header(page)  # => unpack the header before writing anything
    new_upper = pd_upper - len(record)  # => reserve space from the back
    page[new_upper:pd_upper] = record  # => write the record bytes
    struct.pack_into(
        "<HH", page, pd_lower, new_upper, len(record)
    )  # => the slot points AT the record
    slot_index = (
        pd_lower - HEADER_SIZE
    ) // SLOT_SIZE  # => zero-based index of the slot just written
    struct.pack_into(
        "<HH", page, 0, pd_lower + SLOT_SIZE, new_upper
    )  # => advance pd_lower, pd_upper
    return slot_index  # => the handle callers use to read this record back later


def read_by_slot(
    page: bytearray, slot_index: int
) -> bytes:  # => resolves a slot index to record bytes
    slot_pos = (
        HEADER_SIZE + slot_index * SLOT_SIZE
    )  # => byte offset of THIS slot in the array
    off, length = struct.unpack_from(
        "<HH", page, slot_pos
    )  # => the slot's own (offset, length) pair
    return bytes(
        page[int(off) : int(off) + int(length)]
    )  # => slice out exactly `length` bytes


page: bytearray = new_page()  # => one fresh page to insert two records into
idx_a = insert(page, b"alice")  # => slot 0
idx_b = insert(page, b"bob-two")  # => slot 1
print((idx_a, idx_b))  # => Output: (0, 1)
# => slot indexes, NOT byte offsets -- the indirection ex-08 later depends on
print(read_by_slot(page, idx_a))  # => Output: b'alice'
print(read_by_slot(page, idx_b))  # => Output: b'bob-two'

assert (
    read_by_slot(page, idx_a) == b"alice"
)  # => slot 0 resolves to exactly the bytes inserted there
assert (
    read_by_slot(page, idx_b) == b"bob-two"
)  # => slot 1 resolves independently of slot 0
print("ex-05 OK")  # => Output: ex-05 OK

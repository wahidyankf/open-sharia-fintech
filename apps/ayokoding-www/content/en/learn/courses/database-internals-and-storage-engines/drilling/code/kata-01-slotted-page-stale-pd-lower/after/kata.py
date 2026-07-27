"""Kata 1 (after): insert_record writes the new pd_lower/pd_upper back into the header every time."""

from __future__ import annotations

import struct

PAGE_SIZE = 64
HEADER_FORMAT = ">HH"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)


def new_page() -> bytearray:
    page = bytearray(PAGE_SIZE)
    struct.pack_into(HEADER_FORMAT, page, 0, HEADER_SIZE, PAGE_SIZE)
    return page


def insert_record(page: bytearray, record: bytes) -> int:
    pd_lower, pd_upper = struct.unpack_from(HEADER_FORMAT, page, 0)
    slot_count = (pd_lower - HEADER_SIZE) // 4
    new_pd_upper = pd_upper - len(record)
    new_pd_lower = pd_lower + 4
    page[new_pd_upper:pd_upper] = record
    struct.pack_into(">HH", page, pd_lower, new_pd_upper, len(record))
    struct.pack_into(
        HEADER_FORMAT, page, 0, new_pd_lower, new_pd_upper
    )  # => commits the new boundaries
    return slot_count


def read_record(page: bytearray, slot: int) -> bytes:
    slot_offset = HEADER_SIZE + slot * 4
    record_offset, record_length = struct.unpack_from(">HH", page, slot_offset)
    return bytes(page[record_offset : record_offset + record_length])


page = new_page()
slot_a = insert_record(page, b"first")
slot_b = insert_record(page, b"second")
print(slot_a, slot_b)
print(read_record(page, slot_a))

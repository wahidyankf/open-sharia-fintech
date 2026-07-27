"""Kata 1 (before): insert_record forgets to WRITE BACK the new pd_lower, so slot count never advances."""

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
    # BUG: pd_lower's advance is never computed OR written back -- see the "after" fix below
    page[new_pd_upper:pd_upper] = record
    struct.pack_into(">HH", page, pd_lower, new_pd_upper, len(record))
    # BUG: never packs (new_pd_lower, new_pd_upper) back into the header -- pd_lower stays STALE
    return slot_count


def read_record(page: bytearray, slot: int) -> bytes:
    slot_offset = HEADER_SIZE + slot * 4
    record_offset, record_length = struct.unpack_from(">HH", page, slot_offset)
    return bytes(page[record_offset : record_offset + record_length])


page = new_page()
slot_a = insert_record(page, b"first")
slot_b = insert_record(
    page, b"second"
)  # pd_lower never advanced, so this OVERWRITES slot 0's slot entry
print(slot_a, slot_b)
print(
    read_record(page, slot_a)
)  # expected b"first" -- but slot 0's entry was overwritten by the 2nd insert

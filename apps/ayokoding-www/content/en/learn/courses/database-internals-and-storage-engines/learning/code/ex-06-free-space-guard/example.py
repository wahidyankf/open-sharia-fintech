"""Example 6: Guard Against Insufficient Free Space -- insert raises before it corrupts the page."""

import struct  # => stdlib module for packing/unpacking fixed-layout binary fields

PAGE_SIZE: int = 4096  # => same 4 KB page size used throughout this course
HEADER_SIZE: int = 4  # => pd_lower(uint16) + pd_upper(uint16)
SLOT_SIZE: int = 4  # => offset(uint16) + length(uint16) per slot


class PageFullError(Exception):  # => raised instead of silently overwriting live data
    """Raised when a page has too little free space for a new record + slot."""  # => documents the contract


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


def free_space(
    page: bytearray,
) -> int:  # => the gap between the slot array and the tuple data
    pd_lower, pd_upper = header(page)  # => unpack the header before writing anything
    return (
        pd_upper - pd_lower
    )  # => shrinks from BOTH ends as slots and records are added


def insert(
    page: bytearray, record: bytes
) -> int:  # => guarded insert: raises instead of corrupting
    pd_lower, pd_upper = header(page)  # => unpack the header before writing anything
    needed = len(record) + SLOT_SIZE  # => the record AND its slot both need room
    if free_space(page) < needed:  # => the guard: check BEFORE writing anything
        raise PageFullError(
            f"need {needed} bytes, have {free_space(page)}"
        )  # => no write happened
    new_upper = pd_upper - len(
        record
    )  # => safe to reserve room now -- the guard already passed
    page[new_upper:pd_upper] = (
        record  # => write the record's bytes into the reserved gap
    )
    struct.pack_into(
        "<HH", page, pd_lower, new_upper, len(record)
    )  # => point a new slot at it
    struct.pack_into(
        "<HH", page, 0, pd_lower + SLOT_SIZE, new_upper
    )  # => persist the advanced header
    return new_upper  # => the record's offset, same convention as ex-04


page: bytearray = new_page()  # => one fresh, empty page
print(free_space(page))  # => Output: 4092
insert(page, b"x" * 4000)  # => a near-page-sized record: leaves little free space
print(free_space(page))  # => Output: 88
# => 88 bytes left is not nearly enough for a 200-byte record plus its 4-byte slot

raised = False  # => flips to True only if the guard actually fires below
try:
    insert(page, b"y" * 200)  # => 200 + SLOT_SIZE (204) exceeds the remaining 88 bytes
except PageFullError:  # => the exact exception free_space's guard raises
    raised = True  # => confirms the guard fired instead of writing past the page
assert raised  # => the guard fired instead of silently corrupting adjacent bytes
# => nothing on the page changed as a result of the rejected insert attempt
print("ex-06 OK")  # => Output: ex-06 OK

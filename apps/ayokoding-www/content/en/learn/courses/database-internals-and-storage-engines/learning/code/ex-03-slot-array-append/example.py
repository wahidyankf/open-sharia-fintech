"""Example 3: Append a Slot to the Slot Array -- grows from the front of the page."""

import struct

PAGE_SIZE: int = 4096
HEADER_SIZE: int = 4  # => pd_lower(uint16) + pd_upper(uint16)
SLOT_SIZE: int = 4  # => offset(uint16) + length(uint16) per slot

# The slot array grows FORWARD from right after the header; each slot is a
# fixed 4-byte (offset, length) pair pointing at one record's bytes elsewhere
# on the page (co-02). Appending a slot means: write the pair at pd_lower,
# then advance pd_lower past it.


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


def append_slot(
    page: bytearray, offset: int, length: int
) -> int:  # => returns the new pd_lower
    pd_lower, pd_upper = header(page)  # => unpack the header before writing anything
    struct.pack_into(
        "<HH", page, pd_lower, offset, length
    )  # => write the new slot at the OLD pd_lower
    pd_lower += SLOT_SIZE  # => the slot array just grew by one 4-byte entry
    struct.pack_into(
        "<HH", page, 0, pd_lower, pd_upper
    )  # => persist the advanced pd_lower
    return pd_lower  # => callers use this to know how many slots now exist


page: bytearray = new_page()  # => one fresh page to append slots onto
before_lower, _ = header(page)  # => starts at HEADER_SIZE -- zero slots so far
after_first = append_slot(
    page, offset=4090, length=6
)  # => slot 0 -> a 6-byte record near the back
after_second = append_slot(
    page, offset=4080, length=10
)  # => slot 1 -> a 10-byte record
print((before_lower, after_first, after_second))  # => Output: (4, 8, 12)

assert (
    after_first == before_lower + SLOT_SIZE
)  # => one append advances pd_lower by exactly SLOT_SIZE
assert (
    after_second == before_lower + 2 * SLOT_SIZE
)  # => two appends advance it by 2 * SLOT_SIZE
slot_count = (
    after_second - HEADER_SIZE
) // SLOT_SIZE  # => slot count derived from pd_lower's growth
assert slot_count == 2  # => exactly two slots now live in the slot array
print("ex-03 OK")  # => Output: ex-03 OK

"""Example 8: In-Page Compaction After a Delete -- surviving slots still resolve correctly."""

import struct  # => stdlib module for packing/unpacking fixed-layout binary fields

PAGE_SIZE: int = 4096  # => same 4 KB page size used throughout this course
HEADER_SIZE: int = 4  # => pd_lower(uint16) + pd_upper(uint16)
SLOT_SIZE: int = 4  # => offset(uint16) + length(uint16) per slot
DEAD: int = (
    0xFFFF  # => sentinel offset marking a slot as deleted (tombstoned, not removed)
)


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


def slot_count(page: bytearray) -> int:  # => how many slots exist -- live AND deleted
    pd_lower, _ = header(page)  # => only pd_lower is needed for a slot count
    return (
        pd_lower - HEADER_SIZE
    ) // SLOT_SIZE  # => each slot occupies exactly SLOT_SIZE bytes


def insert(
    page: bytearray, record: bytes
) -> int:  # => appends a record, returns its new slot index
    pd_lower, pd_upper = header(page)  # => unpack the header before writing anything
    new_upper = pd_upper - len(record)  # => reserve room from the back
    page[new_upper:pd_upper] = record  # => write the record's bytes
    struct.pack_into(
        "<HH", page, pd_lower, new_upper, len(record)
    )  # => point a new slot at it
    struct.pack_into(
        "<HH", page, 0, pd_lower + SLOT_SIZE, new_upper
    )  # => persist the advanced header
    return (pd_lower - HEADER_SIZE) // SLOT_SIZE  # => this record's new slot index


def delete(
    page: bytearray, slot_index: int
) -> None:  # => tombstones the slot; bytes stay until compaction
    slot_pos = (
        HEADER_SIZE + slot_index * SLOT_SIZE
    )  # => byte offset of this slot in the array
    _, length = struct.unpack_from(
        "<HH", page, slot_pos
    )  # => keep the length -- only the offset dies
    struct.pack_into(
        "<HH", page, slot_pos, DEAD, length
    )  # => offset -> DEAD marks it unreadable


def read(
    page: bytearray, slot_index: int
) -> bytes:  # => resolves a live slot to its record bytes
    slot_pos = (
        HEADER_SIZE + slot_index * SLOT_SIZE
    )  # => byte offset of this slot in the array
    off, length = struct.unpack_from(
        "<HH", page, slot_pos
    )  # => this slot's (offset, length) pair
    if off == DEAD:  # => a tombstoned slot has no live bytes to read
        raise KeyError(
            f"slot {slot_index} is deleted"
        )  # => fail loudly, never return stale bytes
    return bytes(
        page[int(off) : int(off) + int(length)]
    )  # => slice out exactly `length` bytes


def compact(
    page: bytearray,
) -> None:  # => squeezes out the gap a deleted record left behind
    pd_lower, _ = header(
        page
    )  # => the slot array itself does NOT shrink during compaction
    live: list[
        tuple[int, bytes]
    ] = []  # => (slot_index, bytes) for every non-deleted slot
    for i in range(slot_count(page)):  # => walk every slot, live or dead
        slot_pos = HEADER_SIZE + i * SLOT_SIZE  # => byte offset of slot i
        off, length = struct.unpack_from(
            "<HH", page, slot_pos
        )  # => this slot's current (offset, length)
        if (
            off != DEAD
        ):  # => only live slots get carried forward into the compacted layout
            live.append(
                (i, bytes(page[int(off) : int(off) + int(length)]))
            )  # => snapshot its bytes NOW
    write_at = PAGE_SIZE  # => rewrite tuple data from the very back, tightly packed
    for (
        i,
        data,
    ) in live:  # => re-lay live records back-to-back, closing the gap the delete left
        write_at -= len(data)  # => reserve this record's own length before writing it
        page[write_at : write_at + len(data)] = (
            data  # => write the record at its NEW, compacted offset
        )
        slot_pos = (
            HEADER_SIZE + i * SLOT_SIZE
        )  # => the SAME slot position as before -- index unchanged
        struct.pack_into(
            "<HH", page, slot_pos, write_at, len(data)
        )  # => slot now points at the NEW offset
    struct.pack_into(
        "<HH", page, 0, pd_lower, write_at
    )  # => pd_upper reclaims the freed gap


page: bytearray = new_page()  # => one fresh page for a, b, c
a = insert(page, b"row-a")  # => slot 0
b = insert(page, b"row-b-middle")  # => slot 1 -- this one gets deleted below
c = insert(page, b"row-c")  # => slot 2
delete(
    page, b
)  # => tombstones slot 1; its bytes still physically sit on the page for now
compact(page)  # => squeezes slot 1's gap out and rewrites slots 0 and 2 at new offsets
print(read(page, a))  # => Output: b'row-a'
print(read(page, c))  # => Output: b'row-c'

assert (
    read(page, a) == b"row-a"
)  # => slot a still resolves correctly after compaction moved its bytes
assert read(page, c) == b"row-c"  # => slot c still resolves correctly too
_, pd_upper_after = header(page)  # => re-read the header after compaction
assert pd_upper_after == PAGE_SIZE - len(b"row-a") - len(
    b"row-c"
)  # => the deleted record's gap is gone
print("ex-08 OK")  # => Output: ex-08 OK
# => the slot INDEX never changed for either survivor -- only its internal offset did

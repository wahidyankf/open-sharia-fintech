"""Capstone Step 1: slotted-page pack/unpack + a buffer pool.

Time/space complexity per routine (n = records already on a page):

- ``new_page``: O(page_size) -- one zero-filled bytearray allocation.
- ``insert_record`` / ``read_record``: O(record size) -- a fixed-size slot-array
  lookup (co-03) plus a direct byte-range copy; no scan of the other records.
- ``BufferPool.get_page``: O(1) amortized -- a dict lookup on hit; a dict copy
  plus (at most) one eviction on miss.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass, field

PAGE_SIZE = 256  # => a small, illustrative page size (real engines use 4-16 KB, co-01)
HEADER_FORMAT = (
    ">HH"  # => big-endian: pd_lower (slot array end), pd_upper (tuple data start)
)
HEADER_SIZE = struct.calcsize(
    HEADER_FORMAT
)  # => bytes consumed by the page header itself
SLOT_FORMAT = (
    ">HH"  # => each slot: (record_offset, record_length), both unsigned shorts
)


def new_page() -> (
    bytearray
):  # => co-02: header + empty slot array + all-free tuple space
    page = bytearray(PAGE_SIZE)  # => zero-filled -- no records, no slots yet
    struct.pack_into(
        HEADER_FORMAT, page, 0, HEADER_SIZE, PAGE_SIZE
    )  # => pd_lower, pd_upper at start
    return page  # => a fresh, empty page, ready for inserts


def insert_record(
    page: bytearray, record: bytes
) -> int:  # => co-02/co-03: grows slots+data toward each other
    pd_lower, pd_upper = struct.unpack_from(
        HEADER_FORMAT, page, 0
    )  # => current free-space boundaries
    slot_count = (
        pd_lower - HEADER_SIZE
    ) // 4  # => how many slots already exist -- this record's new index
    new_pd_upper = pd_upper - len(
        record
    )  # => tuple data grows DOWNWARD, from the back of the page
    new_pd_lower = (
        pd_lower + 4
    )  # => the slot array grows UPWARD, one 4-byte slot per record
    if (
        new_pd_lower > new_pd_upper
    ):  # => the two boundaries would cross -- no free space left
        raise ValueError(f"page full: cannot fit {len(record)} more bytes")
    page[new_pd_upper:pd_upper] = (
        record  # => the record's bytes land in the newly claimed tuple space
    )
    struct.pack_into(
        SLOT_FORMAT, page, pd_lower, new_pd_upper, len(record)
    )  # => the new slot entry
    struct.pack_into(
        HEADER_FORMAT, page, 0, new_pd_lower, new_pd_upper
    )  # => commit the new boundaries
    return slot_count  # => co-03: callers address this record by SLOT INDEX, not byte offset


def read_record(
    page: bytearray, slot: int
) -> bytes:  # => co-03: slot index -> stable record lookup
    slot_offset = (
        HEADER_SIZE + slot * 4
    )  # => where this slot's own (offset, length) pair lives
    record_offset, record_length = struct.unpack_from(
        SLOT_FORMAT, page, slot_offset
    )  # => indirection
    return bytes(
        page[record_offset : record_offset + record_length]
    )  # => the record's actual bytes


@dataclass
class Frame:  # => co-04: one buffer-pool slot -- a resident page plus its bookkeeping
    page: bytearray  # => the actual page bytes, currently cached in memory
    pin_count: int = 0  # => how many callers currently need this page kept resident
    dirty: bool = (
        False  # => True once this frame's page has been modified since it was loaded
    )


@dataclass
class BufferPool:  # => co-04/co-05/co-06: page table + eviction + a read path that prefers memory
    capacity: int  # => the maximum number of frames this pool may hold at once
    disk: dict[int, bytearray] = field(
        default_factory=dict[int, bytearray]
    )  # => simulated on-disk pages
    frames: dict[int, Frame] = field(
        default_factory=dict[int, Frame]
    )  # => co-04: page_id -> resident frame
    disk_reads: int = 0  # => counts genuine misses -- pages actually loaded from "disk"

    def write_page_to_disk(
        self, page_id: int, page: bytearray
    ) -> None:  # => simulates the underlying store
        self.disk[page_id] = bytearray(
            page
        )  # => a defensive copy -- the disk owns its own bytes

    def get_page(
        self, page_id: int
    ) -> bytearray:  # => co-06: the buffer-pool read path
        frame = self.frames.get(
            page_id
        )  # => co-06: check the pool FIRST, before ever touching disk
        if (
            frame is not None
        ):  # => a hit -- served entirely from memory, no disk I/O at all
            frame.pin_count += (
                1  # => the caller now depends on this page staying resident
            )
            return frame.page
        self.disk_reads += (
            1  # => co-06: a miss -- this is the ONLY path that counts as a disk read
        )
        if (
            len(self.frames) >= self.capacity
        ):  # => the pool is full -- must evict before loading
            self._evict()
        loaded = bytearray(
            self.disk.get(page_id, new_page())
        )  # => load from disk, or a fresh page
        self.frames[page_id] = Frame(
            page=loaded, pin_count=1
        )  # => now resident, pinned for this caller
        return loaded  # => the newly loaded page, ready for the caller to read or write

    def unpin(
        self, page_id: int, mark_dirty: bool = False
    ) -> None:  # => co-05: releases a caller's hold
        frame = self.frames[page_id]  # => the frame this caller was using
        frame.pin_count -= (
            1  # => one fewer caller depends on this page staying resident
        )
        frame.dirty = (
            frame.dirty or mark_dirty
        )  # => once dirty, stays dirty until a flush clears it

    def _evict(self) -> None:  # => co-05: a simple, unpinned-frame-first victim policy
        for page_id, frame in list(
            self.frames.items()
        ):  # => scan for ANY currently unpinned frame
            if (
                frame.pin_count == 0
            ):  # => safe to evict -- nobody is relying on it right now
                if frame.dirty:  # => co-05: a dirty victim must be flushed before its frame is reused
                    self.write_page_to_disk(page_id, frame.page)
                del self.frames[
                    page_id
                ]  # => the frame is now free for a new page to occupy
                return  # => one eviction is enough to make room for the incoming page
        raise RuntimeError("buffer pool full and every frame is pinned -- cannot evict")


def demo() -> (
    None
):  # => a genuine, runnable walkthrough of round-trip + hit-vs-miss behavior
    pool = BufferPool(
        capacity=2
    )  # => a tiny pool, small enough to force an eviction below
    page = pool.get_page(
        page_id=1
    )  # => a MISS -- page 1 does not exist on "disk" yet, so it's fresh
    slot = insert_record(
        page, b"hello-page-1"
    )  # => co-02/co-03: insert one record, remember its slot
    pool.unpin(
        page_id=1, mark_dirty=True
    )  # => release it, marking it dirty since we just wrote to it
    reads_after_first_touch = pool.disk_reads  # => exactly one miss so far
    pool.write_page_to_disk(
        page_id=1, page=pool.frames[1].page
    )  # => persist it, as a real flush would
    hot_page = pool.get_page(
        page_id=1
    )  # => a HIT -- served from the pool, no new disk read
    record = read_record(
        hot_page, slot
    )  # => co-03: slot-indexed read, round-tripping the original bytes
    print(record)  # => the record, byte-for-byte identical to what was inserted
    print(
        reads_after_first_touch, pool.disk_reads
    )  # => the second get_page did NOT increment disk_reads


if (
    __name__ == "__main__"
):  # => only runs the demo when this file is executed directly, not on import
    demo()

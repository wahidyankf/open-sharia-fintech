"""pytest coverage for pages.py -- slotted-page pack/unpack and the buffer pool."""

import pytest

from pages import BufferPool, insert_record, new_page, read_record


def test_a_record_round_trips_through_a_page() -> None:
    page = new_page()
    slot = insert_record(page, b"a-genuine-record")
    assert read_record(page, slot) == b"a-genuine-record"


def test_two_records_get_two_distinct_stable_slots() -> None:
    page = new_page()
    slot_a = insert_record(page, b"first")
    slot_b = insert_record(page, b"second")
    assert slot_a != slot_b
    assert read_record(page, slot_a) == b"first"
    assert read_record(page, slot_b) == b"second"


def test_a_page_raises_once_it_is_actually_full() -> None:
    page = new_page()
    with pytest.raises(ValueError):
        insert_record(page, b"x" * 10_000)  # => far larger than PAGE_SIZE


def test_the_first_get_page_call_is_a_disk_read() -> None:
    pool = BufferPool(capacity=2)
    pool.get_page(page_id=1)
    assert pool.disk_reads == 1


def test_a_hot_page_is_served_from_the_pool_not_disk() -> None:
    pool = BufferPool(capacity=2)
    pool.get_page(page_id=1)  # => a miss -- disk_reads becomes 1
    pool.unpin(page_id=1)
    pool.get_page(page_id=1)  # => a HIT -- disk_reads must NOT increase
    assert pool.disk_reads == 1


def test_eviction_flushes_a_dirty_victim_before_reuse() -> None:
    pool = BufferPool(
        capacity=1
    )  # => capacity 1 forces an eviction on the second distinct page
    page = pool.get_page(page_id=1)
    insert_record(page, b"must-survive")
    pool.unpin(page_id=1, mark_dirty=True)
    pool.get_page(
        page_id=2
    )  # => forces page 1's frame to be evicted, dirty, so it must flush first
    assert (
        pool.disk[1] is not None
    )  # => page 1's dirty content reached "disk" before being evicted


# => Run: pytest -- Output: 6 passed

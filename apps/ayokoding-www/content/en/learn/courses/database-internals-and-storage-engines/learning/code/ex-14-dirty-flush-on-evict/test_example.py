"""Example 14: pytest verification for Flushing a Dirty Page Before Eviction."""

from example import Frame, evict, write


def test_clean_frame_needs_no_flush() -> None:
    disk: dict[int, bytes] = {1: b"same"}
    frame = Frame(page_id=1, data=b"same")  # => never written -- dirty stays False
    evict(frame, disk)
    assert disk[1] == b"same"  # => unchanged, because there was nothing to flush


def test_dirty_frame_is_flushed_before_eviction() -> None:
    disk: dict[int, bytes] = {1: b"old"}
    frame = Frame(page_id=1, data=b"old")
    write(frame, b"new")
    evict(frame, disk)
    assert disk[1] == b"new"  # => the write reached disk exactly at eviction time


# => Run: pytest -- Output: 2 passed

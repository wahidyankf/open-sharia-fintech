"""Example 14: Flush a Dirty Page Before Eviction."""

from dataclasses import dataclass  # => a plain, typed record for one buffer-pool frame


@dataclass  # => auto-generates __init__ from the fields below
class Frame:  # => a buffer-pool frame that tracks whether it needs flushing
    page_id: int  # => which on-disk page this frame currently holds
    data: bytes  # => this frame's current in-memory bytes
    dirty: bool = (
        False  # => True once a WRITE has touched this frame since it was loaded
    )


def write(
    frame: Frame, new_data: bytes
) -> None:  # => the only way a frame's bytes change in memory
    frame.data = (
        new_data  # => the in-memory copy now diverges from whatever disk still holds
    )
    frame.dirty = (
        True  # => marks it as needing a flush before it can safely leave memory
    )


def evict(
    frame: Frame, disk: dict[int, bytes]
) -> None:  # => removes a frame from memory, safely
    if frame.dirty:  # => a dirty frame's changes only exist in memory so far
        disk[frame.page_id] = frame.data  # => flush BEFORE the frame is discarded
    # => a non-dirty (clean) frame already matches disk -- nothing to flush


disk: dict[int, bytes] = {
    7: b"original-on-disk"
}  # => a fake disk with page 7's original bytes
frame = Frame(
    page_id=7, data=b"original-on-disk"
)  # => the same bytes, now also resident in memory
write(frame, b"modified-in-memory")  # => the frame diverges from disk and becomes dirty
assert (
    disk[7] == b"original-on-disk"
)  # => disk has NOT changed yet -- only the in-memory frame has
evict(frame, disk)  # => eviction flushes the dirty frame first
print(disk[7])  # => Output: b'modified-in-memory'

assert (
    disk[7] == b"modified-in-memory"
)  # => the flush happened BEFORE the frame left memory
print("ex-14 OK")  # => Output: ex-14 OK

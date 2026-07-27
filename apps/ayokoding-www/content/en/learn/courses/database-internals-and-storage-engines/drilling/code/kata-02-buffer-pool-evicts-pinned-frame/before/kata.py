"""Kata 2 (before): eviction picks the FIRST frame regardless of pin count, evicting one still in use."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Frame:
    page: bytes
    pin_count: int = 0


@dataclass
class BufferPool:
    capacity: int
    frames: dict[int, Frame] = field(default_factory=dict[int, Frame])
    disk_reads: int = 0

    def get_page(self, page_id: int) -> bytes:
        frame = self.frames.get(page_id)
        if frame is not None:
            frame.pin_count += 1
            return frame.page
        self.disk_reads += 1
        if len(self.frames) >= self.capacity:
            self._evict()
        self.frames[page_id] = Frame(page=f"page-{page_id}".encode(), pin_count=1)
        return self.frames[page_id].page

    def _evict(self) -> None:
        victim = next(
            iter(self.frames)
        )  # BUG: picks the first frame found, never checking pin_count
        del self.frames[victim]


pool = BufferPool(capacity=1)
pool.get_page(1)  # page 1 loaded and PINNED -- a caller still depends on it
pool.get_page(
    2
)  # forces an eviction; the buggy policy evicts page 1 even though it is still pinned
print(
    1 in pool.frames
)  # expected True -- page 1 was pinned and should never have been evicted

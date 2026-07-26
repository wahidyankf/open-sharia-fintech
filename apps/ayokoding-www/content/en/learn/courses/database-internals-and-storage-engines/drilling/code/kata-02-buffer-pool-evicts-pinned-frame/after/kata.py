"""Kata 2 (after): eviction only ever considers a frame whose pin_count is genuinely zero."""

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
        for page_id, frame in list(
            self.frames.items()
        ):  # => scan for an UNPINNED frame specifically
            if frame.pin_count == 0:
                del self.frames[page_id]
                return
        raise RuntimeError("buffer pool full and every frame is pinned -- cannot evict")


pool = BufferPool(capacity=1)
pool.get_page(1)  # page 1 loaded and pinned
try:
    pool.get_page(
        2
    )  # no unpinned victim exists -- fails LOUDLY instead of silently evicting a pinned page
except RuntimeError as error:
    print(error)
print(1 in pool.frames)

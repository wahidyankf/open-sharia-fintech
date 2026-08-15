"""Fixed-size single-file pager with a small LRU cache."""

from __future__ import annotations

import os
from collections import OrderedDict
from pathlib import Path

PAGE_SIZE = 4096


class Pager:
    def __init__(self, path: Path, capacity: int = 2) -> None:
        self.path = path
        self.capacity = capacity
        self.cache: OrderedDict[int, bytes] = OrderedDict()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)

    def read(self, number: int) -> bytes:
        if number in self.cache:
            self.cache.move_to_end(number)
            return self.cache[number]
        with self.path.open("rb") as handle:
            handle.seek(number * PAGE_SIZE)
            page = handle.read(PAGE_SIZE).ljust(PAGE_SIZE, b"\0")
        self.cache[number] = page
        self.cache.move_to_end(number)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
        return page

    def write(self, number: int, page: bytes) -> None:
        if len(page) > PAGE_SIZE:
            raise ValueError("page is larger than PAGE_SIZE")
        data = page.ljust(PAGE_SIZE, b"\0")
        with self.path.open("r+b") as handle:
            handle.seek(number * PAGE_SIZE)
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        self.cache[number] = data
        self.cache.move_to_end(number)

"""Example 74: an LRU-evicting cache -- the FIX for the unbounded cache leak
(ex-36's `_CACHE` dict grew forever; this one evicts once it hits `max_size`)."""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to the fix itself

from collections import (
    OrderedDict,
)  # => co-17: preserves insertion order, so the OLDEST entry is always at the front


class BoundedCache:  # => co-17: replaces ex-36's plain, unbounded dict with one that actually evicts
    def __init__(
        self, max_size: int
    ) -> None:  # => co-17: max_size is the hard cap this cache enforces on every insert
        self._max_size = max_size  # => co-17: the fixed capacity -- never exceeded once get_or_compute() runs
        self._store: OrderedDict[str, str] = (
            OrderedDict()
        )  # => co-17: an ordered dict -- ordering IS the eviction policy

    def get_or_compute(
        self, key: str
    ) -> str:  # => co-17: the SAME public shape as ex-36's leaking version
        if (
            key in self._store
        ):  # => co-17: a cache HIT -- the value already exists, no recomputation needed
            self._store.move_to_end(
                key
            )  # => co-17: mark as recently used -- moves it to the "keep longest" end
            return self._store[
                key
            ]  # => co-17: returns the cached value without touching capacity at all
        value = f"computed-{key}"  # => co-17: a cache MISS -- simulates real work that would be expensive to redo
        self._store[key] = (
            value  # => co-17: inserts the new value at the "most recently used" end
        )
        if (
            len(self._store) > self._max_size
        ):  # => co-17: only evicts once capacity is ACTUALLY exceeded
            self._store.popitem(
                last=False
            )  # => co-17: evict the LEAST recently used entry -- the actual fix over ex-36
        return value  # => co-17: the freshly computed value, now cached (and possibly having evicted an old entry)

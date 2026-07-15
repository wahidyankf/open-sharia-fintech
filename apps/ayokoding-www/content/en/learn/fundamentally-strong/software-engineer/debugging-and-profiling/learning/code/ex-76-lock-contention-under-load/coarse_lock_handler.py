"""Example 76: a function with a COARSE lock -- the whole function body holds
one lock, so concurrent callers serialize on it entirely (a common real-world
mistake: locking too much, not just the truly shared part)."""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to the lock itself

import threading  # => co-21: the primitive whose coarse scope creates the contention this example measures
import time  # => co-21: time.sleep() stands in for real work done "inside" the locked section

_coarse_lock = (
    threading.Lock()
)  # => co-21: ONE lock, shared by every call to handle_request() below


def handle_request(
    work_ms: float,
) -> None:  # => co-21: simulates a "handler" whose whole body is locked, too coarsely
    with _coarse_lock:  # co-21: the ENTIRE function is inside the lock -- too coarse  # => co-21: no work happens OUTSIDE this block
        time.sleep(
            work_ms / 1000
        )  # => co-21: the "work" -- every concurrent caller must wait for this to finish first

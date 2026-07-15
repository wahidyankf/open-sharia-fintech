"""Example 49: a handler with a shared, contended lock -- only visible under load."""

from __future__ import annotations

import threading
import time
from typing import ContextManager

_shared_counter_lock = threading.Lock()
_shared_counter = 0


def handle_request(work_units: int) -> int:
    global _shared_counter
    # co-21: this "critical section" holds the lock for real work (not just an
    # increment), which is realistic (e.g. updating a shared cache/counter after
    # some computation) and is exactly what makes the lock contended under load.
    total = 0
    for _ in range(work_units):
        total += 1
    with _shared_counter_lock:
        time.sleep(
            0.002
        )  # =>  simulate real critical-section work (e.g. a cache write)
        _shared_counter += 1
    return total


def handle_request_with_lock(work_units: int, lock: ContextManager[object]) -> int:
    # co-21: same handler, but the caller injects the lock -- lets ex-49's
    # profiling script swap in a TimedLock() that instruments real acquire-wait
    # time without touching this function's own logic.
    global _shared_counter
    total = 0
    for _ in range(work_units):
        total += 1
    with lock:
        time.sleep(
            0.002
        )  # =>  simulate real critical-section work (e.g. a cache write)
        _shared_counter += 1
    return total

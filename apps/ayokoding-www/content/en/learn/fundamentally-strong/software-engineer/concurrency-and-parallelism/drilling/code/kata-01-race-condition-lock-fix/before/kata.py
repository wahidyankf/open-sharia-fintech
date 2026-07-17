"""Kata 1 (before): a shared page-visit counter loses updates with no lock."""

import threading
import time

VISITS_PER_WORKER = 3_000  # => high enough to reliably widen the race window every run


def record_visits(stats: dict[str, int]) -> None:
    for _ in range(VISITS_PER_WORKER):
        current = stats["count"]  # SMELL: read-modify-write with NO lock around it
        time.sleep(0)  # => yields the GIL right between the read and the write
        stats["count"] = current + 1  # BUG: writes back a possibly-stale `current`


def tally_visits(worker_count: int) -> int:
    stats: dict[str, int] = {"count": 0}
    workers = [threading.Thread(target=record_visits, args=(stats,)) for _ in range(worker_count)]
    for w in workers:
        w.start()  # => all workers now interleave reads/writes to stats["count"] with no coordination
    for w in workers:
        w.join()  # => blocks until every worker's record_visits() call returns
    return stats["count"]


expected = 4 * VISITS_PER_WORKER  # => what the total WOULD be if every increment were counted
actual = tally_visits(4)  # => what the total ACTUALLY is after the unsynchronized race
print(f"expected={expected} actual={actual}")
assert actual < expected  # => confirms at least one increment was lost to the unsynchronized race
print("kata OK (bug reproduced)")

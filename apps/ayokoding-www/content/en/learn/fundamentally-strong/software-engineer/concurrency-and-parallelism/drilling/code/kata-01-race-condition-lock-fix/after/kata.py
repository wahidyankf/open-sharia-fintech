"""Kata 1 (after): a threading.Lock makes the read-modify-write atomic -- no visit is ever lost."""

import threading

VISITS_PER_WORKER = 3_000  # => same workload as the before/ version, for a fair before/after comparison


def record_visits(stats: dict[str, int], guard: threading.Lock) -> None:
    for _ in range(VISITS_PER_WORKER):
        with guard:  # => acquires guard, runs the block, ALWAYS releases -- even if an exception fires
            stats["count"] += 1  # => the whole read-modify-write now happens as ONE atomic step


def tally_visits(worker_count: int) -> int:
    stats: dict[str, int] = {"count": 0}
    guard = threading.Lock()  # => one lock shared by every worker, protecting stats["count"]
    workers = [threading.Thread(target=record_visits, args=(stats, guard)) for _ in range(worker_count)]
    for w in workers:
        w.start()  # => workers now serialize on `guard` for each individual increment
    for w in workers:
        w.join()
    return stats["count"]


expected = 4 * VISITS_PER_WORKER
actual = tally_visits(4)
print(f"expected={expected} actual={actual}")
assert actual == expected  # => every increment survived -- the lock removed the lost-update window
print("kata OK (fix verified)")

"""Example 15: pytest verification for A `Semaphore(2)` Limits Concurrent Access."""

import threading

from example import MAX_CONCURRENT, worker


def test_semaphore_caps_peak_concurrency_at_two() -> None:
    sem = threading.Semaphore(MAX_CONCURRENT)
    lock = threading.Lock()
    active = [0]
    peak = [0]
    threads = [threading.Thread(target=worker, args=(sem, active, peak, lock)) for _ in range(6)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert peak[0] <= MAX_CONCURRENT  # => never more than 2 threads inside at once
    assert peak[0] == MAX_CONCURRENT  # => and it actually used the full allowance


# => Run: pytest -- Output: 1 passed

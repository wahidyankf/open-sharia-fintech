"""Example 33: pytest verification for A Producer Starved by Greedy Consumers."""

import threading
import time

from example import greedy_worker, victim_worker


def test_victim_acquires_far_less_than_greedy_pool() -> None:
    lock = threading.Lock()
    deadline = time.monotonic() + 0.2
    greedy_counters: list[list[int]] = [[0] for _ in range(3)]
    victim_count = [0]
    greedy_threads = [threading.Thread(target=greedy_worker, args=(lock, deadline, greedy_counters[i])) for i in range(3)]
    victim = threading.Thread(target=victim_worker, args=(lock, deadline, victim_count))
    for t in greedy_threads:
        t.start()
    victim.start()
    for t in greedy_threads:
        t.join()
    victim.join()
    total_greedy = sum(counter[0] for counter in greedy_counters)
    assert victim_count[0] < total_greedy  # => the victim is measurably starved


# => Run: pytest -- Output: 1 passed

"""Example 39: pytest verification for Multiple Producers, Multiple Consumers."""

import queue
import threading

from example import consumer, producer


def test_totals_balance_across_multiple_producers_and_consumers() -> None:
    q: "queue.Queue[int | None]" = queue.Queue()
    collected: list[int] = []
    lock = threading.Lock()

    producers = [threading.Thread(target=producer, args=(q, pid, 50)) for pid in range(2)]
    consumers = [threading.Thread(target=consumer, args=(q, collected, lock)) for _ in range(2)]

    for p in producers:
        p.start()
    for c in consumers:
        c.start()
    for p in producers:
        p.join()
    for _ in consumers:
        q.put(None)
    for c in consumers:
        c.join()

    assert len(collected) == 100  # => 2 producers * 50 items each, none lost
    assert len(set(collected)) == 100  # => none duplicated either


# => Run: pytest -- Output: 1 passed

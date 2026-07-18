"""Example 21: pytest verification for A Basic Producer/Consumer Pipeline."""

import queue
import threading

from example import consumer, producer


def test_all_produced_items_are_consumed_in_order() -> None:
    q: "queue.Queue[int]" = queue.Queue()
    total = 15
    results: list[int] = []
    t_p = threading.Thread(target=producer, args=(q, total))
    t_c = threading.Thread(target=consumer, args=(q, total, results))
    t_p.start()
    t_c.start()
    t_p.join()
    t_c.join()
    assert results == list(range(total))  # => every item produced was consumed, in FIFO order


# => Run: pytest -- Output: 1 passed

"""Example 22: pytest verification for A `None` Sentinel Cleanly Shuts Down a Consumer."""

import queue
import threading

from example import consumer, producer


def test_consumer_stops_cleanly_on_sentinel() -> None:
    q: "queue.Queue[int | None]" = queue.Queue()
    items = [7, 8, 9]
    collected: list[int] = []
    t_p = threading.Thread(target=producer, args=(q, items))
    t_c = threading.Thread(target=consumer, args=(q, collected))
    t_p.start()
    t_c.start()
    t_p.join()
    t_c.join(timeout=2)  # => bounded wait -- a hung consumer would fail this assertion, not the test run
    assert collected == items
    assert not t_c.is_alive()  # => the sentinel actually broke the consumer's loop


# => Run: pytest -- Output: 1 passed

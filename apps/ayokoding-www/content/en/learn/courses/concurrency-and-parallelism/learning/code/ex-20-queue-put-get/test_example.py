"""Example 20: pytest verification for `queue.Queue` -- put() and get() Between Threads."""

import queue
import threading

from example import receiver, sender


def test_items_arrive_in_fifo_order() -> None:
    q: "queue.Queue[int]" = queue.Queue()
    items = [1, 2, 3, 4, 5]
    received: list[int] = []
    t_send = threading.Thread(target=sender, args=(q, items))
    t_recv = threading.Thread(target=receiver, args=(q, len(items), received))
    t_recv.start()
    t_send.start()
    t_send.join()
    t_recv.join()
    assert received == items  # => strict FIFO: arrival order matches send order


# => Run: pytest -- Output: 1 passed

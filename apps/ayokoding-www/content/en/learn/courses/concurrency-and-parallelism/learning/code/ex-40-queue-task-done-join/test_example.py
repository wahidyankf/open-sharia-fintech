"""Example 40: pytest verification for `task_done()` + `Queue.join()`."""

import queue
import threading

from example import consumer


def test_join_blocks_until_every_item_is_task_done() -> None:
    q: "queue.Queue[int | None]" = queue.Queue()
    processed = [0]
    worker = threading.Thread(target=consumer, args=(q, processed))
    worker.start()

    for i in range(3):
        q.put(i)
    q.put(None)

    q.join()  # => must not return until all 3 items are task_done()
    assert processed[0] == 3  # => join() waited for the full drain, not just the enqueue

    worker.join(timeout=1)
    assert not worker.is_alive()  # => the consumer also exited cleanly on the sentinel


# => Run: pytest -- Output: 1 passed

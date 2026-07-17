"""Example 38: pytest verification for Bounded Queue Backpressure."""

import queue
import threading

from example import producer


def test_put_nowait_raises_full_at_capacity() -> None:
    q: "queue.Queue[int]" = queue.Queue(maxsize=1)
    q.put_nowait(1)
    try:
        q.put_nowait(2)
        raise AssertionError("expected queue.Full")
    except queue.Full:
        pass  # => confirms a full bounded queue rejects a non-blocking put


def test_blocking_put_waits_until_a_consumer_makes_room() -> None:
    q: "queue.Queue[int]" = queue.Queue(maxsize=1)
    q.put_nowait(0)  # => pre-fill the only slot -- the queue starts at capacity
    finished = [False]
    t = threading.Thread(target=producer, args=(q, [1], finished))
    t.start()
    t.join(timeout=0.2)
    assert finished[0] is False  # => the producer is genuinely blocked, applying backpressure
    q.get()  # => frees a slot
    t.join(timeout=1)
    assert finished[0] is True  # => the producer unblocked once room was made


# => Run: pytest -- Output: 2 passed

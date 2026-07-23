"""Example 19: pytest verification for `Condition` -- wait() and notify()."""

import threading

from example import consumer, producer


def test_consumer_wakes_only_after_producer_notifies() -> None:
    condition = threading.Condition()
    state = {"ready": False}
    trace: list[str] = []
    t_c = threading.Thread(target=consumer, args=(condition, state, trace))
    t_p = threading.Thread(target=producer, args=(condition, state, trace))
    t_c.start()
    t_p.start()
    t_c.join()
    t_p.join()
    assert "consumer-woke" in trace  # => the wait/notify handoff completed
    assert trace.index("producer-set-ready") < trace.index("consumer-woke")  # => strict order


# => Run: pytest -- Output: 1 passed

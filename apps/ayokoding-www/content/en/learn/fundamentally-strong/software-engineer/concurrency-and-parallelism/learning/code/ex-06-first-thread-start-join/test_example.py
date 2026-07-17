"""Example 6: pytest verification for Your First Thread -- start() and join()."""

import threading

from example import worker


def test_join_guarantees_the_worker_finished() -> None:
    log: list[str] = []

    def wrapped() -> None:
        worker()
        log.append("done")

    t = threading.Thread(target=wrapped)
    t.start()
    t.join()
    assert log == ["done"]  # => join() returning means the thread body fully completed
    assert t.is_alive() is False


# => Run: pytest -- Output: 1 passed

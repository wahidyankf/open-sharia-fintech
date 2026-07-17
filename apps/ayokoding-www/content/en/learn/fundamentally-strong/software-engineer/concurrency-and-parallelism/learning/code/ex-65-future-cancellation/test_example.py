"""Example 65: pytest verification for Cancelling a Pending `Future`."""

import threading
from concurrent.futures import Future, ThreadPoolExecutor

from example import never_should_run, occupy_the_only_worker, ran_flag


def test_pending_future_can_be_cancelled_and_never_runs() -> None:
    ran_flag[0] = False  # => resets shared module state before this test's own assertions
    with ThreadPoolExecutor(max_workers=1) as pool:
        release_event = threading.Event()
        occupier: Future[str] = pool.submit(occupy_the_only_worker, release_event)
        pending_future: Future[str] = pool.submit(never_should_run)

        cancelled = pending_future.cancel()
        release_event.set()
        occupier.result()

    assert cancelled is True  # => the cancellation was accepted while the task was still pending
    assert ran_flag[0] is False  # => the cancelled task's body never actually executed
    assert pending_future.cancelled() is True  # => the Future correctly reports itself as cancelled


# => Run: pytest -- Output: 1 passed

"""Example 26: pytest verification for `add_done_callback` Fires on Completion."""

import threading
import time
from concurrent.futures import Future, ThreadPoolExecutor

from example import make_callback, slow_double


def test_callback_runs_after_future_completes() -> None:
    events: list[str] = []
    lock = threading.Lock()
    with ThreadPoolExecutor(max_workers=1) as pool:
        future: "Future[int]" = pool.submit(slow_double, 5)
        future.add_done_callback(make_callback(events, lock))
        future.result()
    time.sleep(0.05)  # => a small grace period in case the callback runs slightly after result()
    assert events == ["done:10"]  # => the callback fired exactly once, with the correct value


# => Run: pytest -- Output: 1 passed

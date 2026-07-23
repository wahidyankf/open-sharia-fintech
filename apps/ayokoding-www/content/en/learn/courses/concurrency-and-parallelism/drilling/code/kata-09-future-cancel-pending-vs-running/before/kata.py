"""Kata 9 (before): calling cancel() on an ALREADY-RUNNING Future silently fails -- the caller never notices."""

import threading
import time
from concurrent.futures import ThreadPoolExecutor, Future


def slow_job(started: threading.Event) -> str:
    started.set()  # => signals the main thread that this job has genuinely started running
    time.sleep(0.2)  # => simulates real work in progress -- NOT cancellable mid-flight by Future.cancel()
    return "done"


started = threading.Event()
with ThreadPoolExecutor(max_workers=1) as pool:  # => max_workers=1 -- the job starts running IMMEDIATELY
    future: Future[str] = pool.submit(slow_job, started)
    started.wait(timeout=1.0)  # => blocks until slow_job() has ACTUALLY started (not just been submitted)
    # SMELL: cancel() is called with no check of its return value, assuming it always "worked"
    cancelled = future.cancel()  # BUG: a RUNNING future cannot be cancelled -- this returns False
    print(f"cancelled={cancelled}")
    result = future.result()  # => the job runs to completion regardless -- "done", not a CancelledError
    print(f"result={result}")

assert cancelled is False  # => confirms cancel() silently failed on an already-running future
assert result == "done"  # => confirms the job ran to completion anyway, unaffected by the cancel() call
print("kata OK (bug reproduced)")

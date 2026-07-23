"""Kata 9 (after): cancel() a genuinely PENDING (not-yet-started) Future -- and always check the return value."""

import threading
import time
from concurrent.futures import ThreadPoolExecutor, Future


def slow_job(started: threading.Event) -> str:
    started.set()
    time.sleep(0.2)
    return "done"


def queued_job() -> str:
    return "should never run"  # => only reachable if the cancel() below fails


started = threading.Event()
with ThreadPoolExecutor(max_workers=1) as pool:  # => FIX: only ONE worker -- job_a occupies it immediately
    job_a: Future[str] = pool.submit(slow_job, started)  # => starts running right away, occupying the sole worker
    started.wait(timeout=1.0)  # => confirms job_a has genuinely started
    job_b: Future[str] = pool.submit(queued_job)  # FIX: job_b is now genuinely PENDING -- the worker is busy
    cancelled = job_b.cancel()  # => job_b never started, so cancel() succeeds
    print(f"cancelled={cancelled}")
    if not cancelled:  # FIX: the caller now actually CHECKS the return value, instead of assuming success
        job_b.result()  # => only reached if cancellation genuinely failed
    job_a.result()  # => job_a still runs to completion -- it was never a cancellation candidate

assert cancelled is True  # => confirms job_b, still pending, was successfully cancelled
assert job_b.cancelled() is True  # => the Future itself confirms its own cancelled state
print("kata OK (fix verified)")

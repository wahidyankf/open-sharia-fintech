"""Example 15: A `Semaphore(2)` Limits Concurrent Access."""  # => co-13: a counter permitting at most N holders

import threading  # => threading.Semaphore -- a counter permitting at most N concurrent holders
import time  # => used to hold the section open long enough to observe overlapping threads

MAX_CONCURRENT = 2  # => the semaphore's permit count -- at most this many threads inside at once


def worker(sem: threading.Semaphore, active: list[int], peak: list[int], lock: threading.Lock) -> None:
    # => sem: the shared Semaphore; active/peak: shared bookkeeping; lock: guards THAT bookkeeping
    with sem:  # => acquires a permit -- blocks if MAX_CONCURRENT are already inside
        with lock:  # => a SEPARATE lock, just to safely update the shared bookkeeping below
            active[0] += 1  # => one more thread is now inside the semaphore-guarded section
            peak[0] = max(peak[0], active[0])  # => peak[0]: the highest concurrency EVER observed
        time.sleep(0.05)  # => holds the section open, giving other threads a chance to overlap
        with lock:  # => re-acquires the bookkeeping lock to record this thread leaving
            active[0] -= 1  # => this thread is about to release its permit


if __name__ == "__main__":  # => module entry point
    semaphore = threading.Semaphore(MAX_CONCURRENT)  # => permits exactly MAX_CONCURRENT holders at once
    bookkeeping_lock = threading.Lock()  # => protects `active`/`peak` from their OWN race (co-11)
    active_count = [0]  # => how many threads are INSIDE the semaphore section right now
    peak_count = [0]  # => the highest `active_count` reached during the whole run
    threads = [  # => builds 6 Thread objects, all sharing the SAME semaphore and bookkeeping
        threading.Thread(target=worker, args=(semaphore, active_count, peak_count, bookkeeping_lock))
        # => each thread's args tuple wires it to the shared semaphore/active/peak/lock state
        for _ in range(6)  # => 6 threads compete for only 2 concurrent slots
    ]  # => threads: a list of exactly 6 Thread objects, not yet started
    for t in threads:  # => launches all 6 threads
        t.start()  # => all 6 immediately try to acquire the semaphore
    for t in threads:  # => waits for all 6 to finish
        t.join()  # => join() blocks until that thread's worker() call returns

    print(f"peak_concurrency={peak_count[0]}")  # => Output: peak_concurrency=2
    # => the bookkeeping lock and the semaphore protect DIFFERENT things: one data, one concurrency.
    assert peak_count[0] <= MAX_CONCURRENT  # => confirms the semaphore NEVER let more than 2 in at once
    assert peak_count[0] == MAX_CONCURRENT  # => confirms it actually reached the full allowed concurrency
    print("ex-15 OK")  # => Output: ex-15 OK

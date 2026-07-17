"""Example 33: A Producer Starved by Greedy Consumers."""

import threading  # => co-17: starvation -- one thread perpetually denied its turn, unlike livelock
import time  # => bounds how long the demo runs

RUN_SECONDS = 0.3  # => how long the greedy threads and the victim compete for the SAME lock


def greedy_worker(lock: threading.Lock, stop_at: float, acquisitions: list[int]) -> None:
    # => acquisitions: a length-1 list shared with ONE specific greedy thread, used as a mutable box
    while time.monotonic() < stop_at:  # => keeps running until the shared deadline passes
        with lock:  # => immediately re-acquires the SAME lock the instant it's free
            acquisitions[0] += 1  # => counts one more successful acquisition by this greedy thread
            # => does essentially NO work inside the critical section -- just grabs it and lets go


def victim_worker(lock: threading.Lock, stop_at: float, acquisitions: list[int]) -> None:
    while time.monotonic() < stop_at:  # => keeps trying for the same deadline as the greedy threads
        time.sleep(0.001)  # => the victim politely waits a beat before EVERY attempt -- its only "flaw"
        with lock:  # => competes for the exact same lock the greedy threads are hammering
            acquisitions[0] += 1  # => counts one more successful acquisition by the victim


if __name__ == "__main__":  # => module entry point
    shared_lock = threading.Lock()  # => the single contended resource every thread wants
    deadline = time.monotonic() + RUN_SECONDS  # => deadline: the shared stop time for all threads
    greedy_counters: list[list[int]] = [[0] for _ in range(3)]  # => one PRIVATE single-item list per greedy thread
    victim_count = [0]  # => the victim's own acquisition counter
    greedy_threads = [
        threading.Thread(target=greedy_worker, args=(shared_lock, deadline, greedy_counters[i]))
        for i in range(3)  # => THREE greedy threads, all hammering the lock nonstop
    ]  # => greedy_threads: a list of exactly 3 Thread objects, not yet started
    victim = threading.Thread(target=victim_worker, args=(shared_lock, deadline, victim_count))
    # => victim: a SINGLE thread, deliberately outnumbered 3-to-1 by the greedy pool above
    for t in greedy_threads:  # => launches all three greedy threads
        t.start()  # => each immediately starts hammering `shared_lock` with zero delay between tries
    victim.start()  # => starts the victim -- politely sleeps 1ms before every single attempt
    for t in greedy_threads:  # => waits for every greedy thread to hit the deadline
        t.join()  # => join() blocks until that greedy thread's loop exits
    victim.join()  # => waits for the victim's loop to exit too

    total_greedy = sum(counter[0] for counter in greedy_counters)  # => sums all 3 greedy threads' own counters
    print(f"total_greedy={total_greedy} victim={victim_count[0]}")  # => Output: total_greedy=<big> victim=<small>

    # => The greedy threads re-acquire the lock the INSTANT it's free, with no gap. The victim
    # => always sleeps 1ms first, so by the time it tries, a greedy thread has usually already
    # => grabbed the lock again -- the victim gets crowded out far more than its "fair" 1-of-4 share.
    assert victim_count[0] < total_greedy  # => confirms the victim acquired far fewer times than the greedy pool
    print("ex-33 OK")  # => Output: ex-33 OK

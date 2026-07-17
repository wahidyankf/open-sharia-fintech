"""Kata 9 (before): state-fault-line violation -- two threads share one mutable counter and lose an update."""

import threading


class PageViewCounter:
    def __init__(self) -> None:
        self.views = 0  # SMELL: one shared mutable box, read-then-written by two threads


def record_view(counter: PageViewCounter, read_done: threading.Event, may_write: threading.Event) -> None:
    current = counter.views  # STEP 1: read the shared value
    read_done.set()  # signal "I have read" -- forces a specific, deterministic interleaving
    may_write.wait()  # STEP 2: wait until it's safe to write (forces the race window open)
    counter.views = current + 1  # BUG: STEP 3 writes back based on the STALE value read in step 1


counter = PageViewCounter()
event_a_read = threading.Event()
event_b_read = threading.Event()
thread_a = threading.Thread(target=record_view, args=(counter, event_a_read, event_b_read))
thread_b = threading.Thread(target=record_view, args=(counter, event_b_read, event_a_read))
# Each thread waits on the OTHER thread's "read done" signal before it's allowed to write -- this
# deterministically forces BOTH threads to read 0 before EITHER of them writes 1, every single run.
thread_a.start()
thread_b.start()
thread_a.join()
thread_b.join()

print(counter.views)  # two views were recorded, but only ONE survived -- a lost update

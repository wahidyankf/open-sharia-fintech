"""Example 18: A `Barrier` Rendezvous Point."""  # => co-15: an N-way meeting point -- no one passes until all arrive

import threading  # => threading.Barrier -- an N-way rendezvous, no thread passes until ALL arrive
import time  # => proves early arrivers genuinely waited, not just finished quickly by chance

PARTIES = 4  # => how many threads must arrive before ANY of them is released


def arrive(barrier: threading.Barrier, arrival_order: list[int], worker_id: int, delay: float) -> None:
    # => worker_id identifies this thread; delay staggers WHEN it reaches the barrier
    time.sleep(delay)  # => staggers arrivals -- some threads reach the barrier before others
    barrier.wait()  # => BLOCKS until all PARTIES threads have called wait() -- then releases them ALL
    arrival_order.append(worker_id)  # => recorded only AFTER the barrier released this thread


if __name__ == "__main__":  # => module entry point
    barrier = threading.Barrier(PARTIES)  # => requires exactly PARTIES threads before releasing any
    order: list[int] = []  # => records the order threads pass the barrier -- NOT the order they arrive
    delays = [0.05, 0.15, 0.25, 0.35]  # => four different arrival times -- deliberately staggered
    threads = [  # => builds one thread per (worker_id, delay) pair, all sharing the SAME barrier
        threading.Thread(target=arrive, args=(barrier, order, i, delays[i]))
        # => each thread's args wire it to its own worker_id and delay, sharing ONE barrier
        for i in range(PARTIES)  # => one thread per party -- exactly matches the barrier's count
    ]  # => threads: a list of exactly PARTIES Thread objects, not yet started
    for t in threads:  # => launches all four threads
        t.start()  # => each begins its own staggered sleep before reaching the barrier
    for t in threads:  # => waits for all four to finish
        t.join()  # => join() blocks until that thread's arrive() call fully returns

    print(sorted(order))  # => Output: [0, 1, 2, 3]
    # => a Barrier is reusable (unlike a one-shot Event) -- it resets automatically after each release.
    assert len(order) == PARTIES  # => confirms every thread eventually passed the barrier
    assert sorted(order) == list(range(PARTIES))  # => confirms every worker_id passed exactly once
    print("ex-18 OK")  # => Output: ex-18 OK

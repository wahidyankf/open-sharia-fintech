"""Example 38: A Bounded Queue Applies Backpressure to a Fast Producer."""

import queue  # => co-22: `Queue(maxsize=N)` is the standard way to bound in-flight work
import threading  # => runs the producer on its own thread so the main thread can observe blocking

MAX_SIZE = 2  # => the queue can hold at most 2 items before `put()` starts blocking


def producer(q: "queue.Queue[int]", items: list[int], put_returned: list[bool]) -> None:
    for item in items:  # => tries to enqueue every item, one at a time
        q.put(item)  # => BLOCKS once the queue is full, until a consumer calls get() to make room
    put_returned[0] = True  # => only set AFTER the final put() returns -- proves the producer finished


if __name__ == "__main__":  # => module entry point
    bounded_queue: "queue.Queue[int]" = queue.Queue(maxsize=MAX_SIZE)  # => the bounded channel under test
    bounded_queue.put_nowait(100)  # => fills slot 1 immediately, without blocking (queue not full yet)
    bounded_queue.put_nowait(200)  # => fills slot 2 -- the queue is now AT capacity (maxsize=2)
    try:
        bounded_queue.put_nowait(300)  # => a THIRD item, attempted without blocking
        raise AssertionError("expected queue.Full")  # => should never reach here -- see except below
    except queue.Full:  # => queue.Full: raised because put_nowait refuses to block, and there's no room
        print("put_nowait raised queue.Full at capacity")  # => Output: put_nowait raised queue.Full at capacity

    finished = [False]  # => flips to True only once the blocking producer thread's LAST put() returns
    still_full_queue: "queue.Queue[int]" = queue.Queue(maxsize=MAX_SIZE)  # => a fresh queue for the blocking-put demo
    still_full_queue.put_nowait(1)  # => pre-fill slot 1
    still_full_queue.put_nowait(2)  # => pre-fill slot 2 -- the queue starts already AT capacity
    slow_producer = threading.Thread(target=producer, args=(still_full_queue, [3], finished))
    slow_producer.start()  # => calls the BLOCKING put(3) -- the queue has no room, so this must block

    slow_producer.join(timeout=0.2)  # => waits briefly -- NOT long enough for a real consumer to intervene
    print(f"producer_finished_before_any_get={finished[0]}")  # => Output: producer_finished_before_any_get=False
    # => finished[0] is STILL False: the producer's put(3) is genuinely blocked, applying backpressure

    drained_item = still_full_queue.get()  # => makes room by draining ONE item -- unblocks the producer
    slow_producer.join(timeout=1)  # => NOW the blocked put(3) can complete, so join should return promptly
    print(f"drained={drained_item} producer_finished_after_get={finished[0]}")
    # => Output: drained=1 producer_finished_after_get=True

    # => Backpressure means the PRODUCER slows down to match the CONSUMER's pace, automatically, with
    # => no extra code: `Queue(maxsize=N)` makes `put()` block once the buffer is full, and unblock the
    # => instant a consumer frees a slot. This prevents unbounded memory growth when a producer is
    # => faster than its consumer -- the queue's bound becomes the system's natural speed limiter.
    assert finished[0] is True  # => confirms the blocked producer eventually completed, after get() freed a slot
    assert not slow_producer.is_alive()  # => confirms the producer thread actually finished, not still stuck
    print("ex-38 OK")  # => Output: ex-38 OK

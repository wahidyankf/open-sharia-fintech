"""Example 40: `task_done()` + `Queue.join()` -- Waiting for a Full Drain."""

import queue  # => co-21/co-22: `Queue.join()` blocks until every item has been marked `task_done()`
import threading  # => the consumer runs on its own thread while the main thread waits on `join()`
import time  # => a tiny per-item delay makes the "main thread genuinely waited" effect observable

ITEM_COUNT = 5  # => how many items the producer enqueues before the main thread calls join()


def consumer(q: "queue.Queue[int | None]", processed: list[int]) -> None:
    while True:  # => runs forever, pulling items until told to stop
        item = q.get()  # => blocks until an item (or the sentinel) is available
        if item is None:  # => None is the shutdown sentinel for this consumer
            q.task_done()  # => the sentinel itself must ALSO be marked done, or join() would hang on it
            break  # => stops the consumer loop
        time.sleep(0.01)  # => simulates a small amount of "work" per item, so draining takes measurable time
        processed[0] += 1  # => records that this item was FULLY processed, not just dequeued
        q.task_done()  # => tells the queue's internal counter this item is DONE -- required for join() to unblock


if __name__ == "__main__":  # => module entry point
    work_queue: "queue.Queue[int | None]" = queue.Queue()  # => the queue whose drain the main thread will await
    processed_count = [0]  # => how many items the consumer has actually finished (not just received)

    worker = threading.Thread(target=consumer, args=(work_queue, processed_count))
    worker.start()  # => starts the consumer -- it immediately blocks on q.get() since the queue is empty

    for i in range(ITEM_COUNT):  # => enqueues ITEM_COUNT real work items
        work_queue.put(i)  # => each put() wakes the consumer if it was blocked waiting
    work_queue.put(None)  # => enqueues the sentinel LAST, so it's processed only after every real item

    print(f"before_join processed={processed_count[0]}")  # => Output: before_join processed=<0 or a small number>
    work_queue.join()  # => BLOCKS the main thread until every put() item has a matching task_done()
    print(f"after_join processed={processed_count[0]}")  # => Output: after_join processed=5
    # => join() only returned once ALL 5 real items AND the sentinel were marked task_done()

    worker.join(timeout=1)  # => also waits for the consumer thread itself to fully exit its loop

    # => `task_done()` decrements the queue's internal "unfinished tasks" counter; `join()` blocks the
    # => calling thread until that counter reaches zero. This lets the MAIN thread wait for a complete
    # => drain without needing to know how many consumer threads exist or coordinate any extra Event --
    # => the queue itself tracks completion, as long as every get() is paired with a task_done().
    assert processed_count[0] == ITEM_COUNT  # => confirms join() did NOT return early -- every item was done
    print("ex-40 OK")  # => Output: ex-40 OK

"""Example 78: Graceful Shutdown -- Draining In-Flight Work Before a Worker Pool Exits."""

import queue  # => co-22, co-23: sentinels drive the drain, exactly like ex-22's shutdown pattern
import threading  # => a small pool of workers, all sharing one queue

WORK_ITEM_COUNT = 30  # => how many items are queued before the "shutdown signal" arrives
WORKER_COUNT = 3  # => how many worker threads process the queue concurrently


def worker(q: "queue.Queue[int | None]", results: list[int], lock: threading.Lock) -> None:
    while True:  # => keeps draining until this worker's OWN sentinel arrives
        item = q.get()  # => blocks until an item (real work, or a shutdown sentinel) is ready
        if item is None:  # => None: the graceful-shutdown sentinel for THIS worker
            break  # => stops ONLY this worker -- others keep draining their own remaining items
        with lock:  # => `results` is SHARED across all worker threads -- needs a lock
            results.append(item)  # => records the completed item -- this IS the "in-flight work" finishing


def run_with_graceful_shutdown(work_items: list[int]) -> list[int]:
    q: "queue.Queue[int | None]" = queue.Queue()  # => q: holds every real work item, queued up front
    for item in work_items:  # => enqueues ALL the real work BEFORE any worker even starts
        q.put(item)  # => every item is in the queue before "the signal" below is simulated

    results: list[int] = []  # => results: filled in by whichever worker actually processes each item
    lock = threading.Lock()  # => protects `results.append` across the WORKER_COUNT worker threads
    workers = [threading.Thread(target=worker, args=(q, results, lock)) for _ in range(WORKER_COUNT)]
    for w in workers:  # => starts every worker thread
        w.start()  # => each begins pulling and processing items from the SAME shared queue

    # => a real signal handler (e.g. for SIGTERM) would run HERE, asynchronously, mid-drain --
    # => this is simulated by simply queuing the sentinels immediately, AFTER the real work, but
    # => WITHOUT waiting for the queue to empty first: workers may still be mid-item when this runs
    for _ in range(WORKER_COUNT):  # => enqueues exactly one shutdown sentinel PER worker
        q.put(None)  # => "graceful" because it's queued, NOT injected ahead of the real work already there

    for w in workers:  # => waits for every worker to drain its remaining real items AND its sentinel
        w.join()  # => join() blocks until that worker's while-loop breaks on its own None

    return results  # => every item that was in the queue BEFORE shutdown, now fully processed


if __name__ == "__main__":  # => module entry point
    work_items = list(range(WORK_ITEM_COUNT))  # => work_items: the full batch of "in-flight" work
    results = run_with_graceful_shutdown(work_items)  # => drives the whole graceful-shutdown scenario
    print(f"processed={len(results)} expected={WORK_ITEM_COUNT}")  # => Output: processed=30 expected=30

    # => Because the shutdown sentinels are APPENDED to the queue rather than injected ahead of the
    # => real work, every item queued BEFORE shutdown is guaranteed to be processed first -- a worker
    # => only sees its sentinel (and exits) AFTER draining every real item that was ahead of it (co-22).
    # => This "sentinel-based drain" is the simplest correct pattern for graceful shutdown: signal
    # => handlers stop NEW work from being accepted, while a queue's own FIFO ordering (co-23) ensures
    # => nothing already in flight is dropped.
    assert sorted(results) == work_items  # => confirms EVERY queued item was processed, none dropped
    assert len(results) == WORK_ITEM_COUNT  # => confirms nothing was processed twice either
    print("ex-78 OK")  # => Output: ex-78 OK

"""Example 39: Several Producers and Several Consumers, One Shared Queue."""

import queue  # => co-22: `Queue` is thread-safe by design, so MANY threads can share ONE instance
import threading  # => runs 3 producers and 3 consumers concurrently against the same queue

ITEMS_PER_PRODUCER = 200  # => each producer contributes this many items
# => total real items produced = NUM_PRODUCERS * ITEMS_PER_PRODUCER, computed once below as `expected_total`
NUM_PRODUCERS = 3  # => three independent producer threads
NUM_CONSUMERS = 3  # => three independent consumer threads


def producer(q: "queue.Queue[int | None]", producer_id: int, count: int) -> None:
    for i in range(count):  # => generates `count` globally-unique item ids for THIS producer
        q.put(producer_id * 100_000 + i)  # => encodes producer_id into the value so ids never collide


def consumer(q: "queue.Queue[int | None]", collected: list[int], lock: threading.Lock) -> None:
    while True:  # => keeps draining until this consumer's OWN sentinel arrives
        item = q.get()  # => BLOCKS if the queue is momentarily empty -- fine, another producer will fill it
        if item is None:  # => None is this consumer's sentinel -- exactly one per consumer is enqueued below
            break  # => stops THIS consumer only -- the other consumers keep running on their own sentinels
        with lock:  # => `collected` is a plain list SHARED across all consumer threads -- needs a lock
            collected.append(item)  # => records the item this consumer just pulled off the shared queue


if __name__ == "__main__":  # => module entry point
    shared_queue: "queue.Queue[int | None]" = queue.Queue()  # => the ONE queue every producer/consumer thread shares
    collected: list[int] = []  # => accumulates EVERY item any consumer pulled, across all consumers
    collect_lock = threading.Lock()  # => protects `collected.append` from concurrent consumer writes

    producers = [
        # => list comprehension: builds NUM_PRODUCERS Thread objects, one per distinct producer_id
        threading.Thread(target=producer, args=(shared_queue, pid, ITEMS_PER_PRODUCER))
        for pid in range(NUM_PRODUCERS)  # => builds one Thread per producer, not yet started
    ]  # => producers: exactly NUM_PRODUCERS Thread objects, each with a distinct producer_id
    consumers = [
        # => list comprehension: builds NUM_CONSUMERS Thread objects, all sharing the SAME arguments
        threading.Thread(target=consumer, args=(shared_queue, collected, collect_lock))
        for _ in range(NUM_CONSUMERS)  # => the consumer id itself doesn't matter -- all consume identically
    ]  # => consumers: exactly NUM_CONSUMERS Thread objects, all sharing `collected` and `collect_lock`

    for p in producers:  # => starts every producer thread
        p.start()  # => each producer begins pushing its own ITEMS_PER_PRODUCER items into shared_queue
    for c in consumers:  # => starts every consumer thread
        c.start()  # => each consumer begins pulling items -- whichever producer's item happens to be next
    for p in producers:  # => waits for every producer to finish generating its items
        p.join()  # => join() blocks until that producer's loop has enqueued all its items

    for _ in range(NUM_CONSUMERS):  # => enqueues exactly one sentinel PER consumer, so each one can stop
        shared_queue.put(None)  # => None: the shutdown signal -- only sent after ALL real items are queued
    for c in consumers:  # => waits for every consumer to drain its sentinel and exit
        c.join()  # => join() blocks until that consumer's while-loop breaks on its own None

    expected_total = NUM_PRODUCERS * ITEMS_PER_PRODUCER  # => expected_total: how many REAL items were produced
    print(f"expected={expected_total} collected={len(collected)} unique={len(set(collected))}")
    # => Output: expected=600 collected=600 unique=600

    # => Multiple producers and multiple consumers can safely share ONE `queue.Queue` instance --
    # => the queue's internal lock serializes every put/get, so items are never duplicated or corrupted
    # => even though 6 threads are hammering it at once. The totals balance: every item any producer
    # => made is picked up by EXACTLY one consumer, and the set of collected ids has no duplicates.
    assert len(collected) == expected_total  # => confirms no item was lost or double-delivered
    assert len(set(collected)) == expected_total  # => confirms every collected id is unique -- no duplicates
    print("ex-39 OK")  # => Output: ex-39 OK

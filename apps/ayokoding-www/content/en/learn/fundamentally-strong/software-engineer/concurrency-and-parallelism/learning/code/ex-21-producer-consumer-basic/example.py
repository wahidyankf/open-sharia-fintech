"""Example 21: A Basic Producer/Consumer Pipeline."""  # => co-22: decoupling producers from consumers via a queue

import queue  # => the bounded buffer decoupling producer from consumer (co-22)
import threading  # => one producer thread, one consumer thread


def producer(q: "queue.Queue[int]", count: int) -> None:  # => produces `count` items, one per put()
    for i in range(count):  # => generates items 0, 1, 2, ..., count - 1
        q.put(i)  # => hands the item off -- the producer never needs to know who consumes it


def consumer(q: "queue.Queue[int]", count: int, collected: list[int]) -> None:  # => consumes `count` items
    for _ in range(count):  # => pulls exactly `count` items -- matches the producer's total
        collected.append(q.get())  # => get() blocks until the producer has something ready


if __name__ == "__main__":  # => module entry point
    pipeline: "queue.Queue[int]" = queue.Queue()  # => the decoupling buffer between the two roles
    total_items = 10  # => how many items the producer generates, and the consumer must collect
    results: list[int] = []  # => every item the consumer actually received, in arrival order
    t_prod = threading.Thread(target=producer, args=(pipeline, total_items))  # => generates work
    t_cons = threading.Thread(target=consumer, args=(pipeline, total_items, results))  # => does work
    t_prod.start()  # => starts producing immediately
    t_cons.start()  # => starts consuming -- overlaps with production via the queue
    t_prod.join()  # => waits for production to finish
    t_cons.join()  # => waits for consumption to finish

    print(results)  # => Output: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # => neither thread ever calls the other directly -- the queue is the ONLY coupling between them.
    assert len(results) == total_items  # => confirms EVERY produced item was eventually consumed
    assert results == list(range(total_items))  # => confirms items were consumed in FIFO order
    print("ex-21 OK")  # => Output: ex-21 OK

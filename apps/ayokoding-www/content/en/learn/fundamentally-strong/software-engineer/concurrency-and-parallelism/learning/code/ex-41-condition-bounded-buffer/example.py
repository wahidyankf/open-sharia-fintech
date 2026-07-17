"""Example 41: A Hand-Built Bounded Buffer, Using `Condition` Directly."""

import threading  # => co-14: builds the SAME guarantee as `queue.Queue(maxsize=N)`, but by hand
from collections import deque  # => deque: an efficient double-ended queue for the buffer's backing storage


class BoundedBuffer:  # => a minimal reimplementation of what ex-38's Queue(maxsize=N) does internally
    def __init__(self, capacity: int) -> None:
        # => capacity: the fixed maximum size -- never changes after construction
        self._capacity = capacity  # => _capacity: the maximum number of items this buffer may hold
        self._items: deque[int] = deque()  # => _items: the actual storage, protected by _condition below
        self._condition = threading.Condition()  # => ONE Condition guards BOTH "not full" and "not empty"

    def put(self, item: int) -> None:
        # => blocks the CALLING thread (not the whole process) whenever the buffer is at capacity
        with self._condition:  # => acquires the Condition's internal lock for the whole critical section
            while len(self._items) >= self._capacity:  # => a WHILE loop, not an if -- guards against spurious wakeups
                self._condition.wait()  # => releases the lock and sleeps until notified; re-acquires on wake
            self._items.append(item)  # => now there IS room -- safe to add
            self._condition.notify_all()  # => wakes any waiting get() calls -- there's a new item to consume

    def get(self) -> int:
        # => the mirror image of put() -- blocks the CALLING thread whenever the buffer is empty
        with self._condition:  # => acquires the SAME lock -- only one thread runs this block at a time
            while not self._items:  # => a WHILE loop again -- re-checks the predicate after every wakeup
                self._condition.wait()  # => releases the lock and sleeps until notified; re-acquires on wake
            item = self._items.popleft()  # => item: the OLDEST item -- popleft() preserves FIFO ordering
            self._condition.notify_all()  # => wakes any waiting put() calls -- there's now room for one more
            return item  # => hands the item back to the caller


def producer(buffer: BoundedBuffer, items: list[int]) -> None:
    for item in items:  # => pushes each item in turn, blocking via Condition.wait() whenever full
        buffer.put(item)  # => put() only returns once the item has actually been stored


def consumer(buffer: BoundedBuffer, count: int, collected: list[int]) -> None:
    for _ in range(count):  # => pulls exactly `count` items, blocking via Condition.wait() whenever empty
        collected.append(buffer.get())  # => get() only returns once an item has actually been retrieved


if __name__ == "__main__":  # => module entry point
    buffer = BoundedBuffer(capacity=3)  # => a buffer that can hold at most 3 items at once
    produced = list(range(20))  # => produced: 20 items to push through the buffer, in order
    collected: list[int] = []  # => collected: what the consumer actually retrieved, in the order retrieved

    p = threading.Thread(target=producer, args=(buffer, produced))
    # => p: the single producer thread, pushing all 20 items through the SAME buffer instance
    c = threading.Thread(target=consumer, args=(buffer, len(produced), collected))
    # => c: the single consumer thread, pulling exactly len(produced) items back out
    p.start()  # => starts pushing items -- blocks on put() once the buffer holds 3
    c.start()  # => starts pulling items -- blocks on get() whenever the buffer is empty
    p.join()  # => waits for every item to be pushed
    c.join()  # => waits for every item to be pulled

    print(f"produced={produced[:5]}... collected={collected[:5]}...")  # => Output: produced=[0,1,2,3,4]... collected=[0,1,2,3,4]...

    # => A hand-built Condition-based buffer needs the SAME two ingredients as `queue.Queue`: a shared
    # => lock (the Condition's own lock) and a WHILE-loop predicate check around every wait() (co-14) --
    # => an `if` would miss a spurious wakeup or a stale notification. Done right, FIFO order and the
    # => capacity bound both hold, exactly like the built-in Queue this reimplements from scratch.
    assert collected == produced  # => confirms strict FIFO delivery -- nothing reordered, lost, or duplicated
    print("ex-41 OK")  # => Output: ex-41 OK

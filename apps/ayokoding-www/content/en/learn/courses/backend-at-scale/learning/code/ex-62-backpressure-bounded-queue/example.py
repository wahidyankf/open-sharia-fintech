# pyright: strict
"""Example 62: Backpressure -- a bounded queue blocks the producer. (co-31)

A bounded queue caps in-flight work so a fast producer cannot overwhelm a
slow consumer. When the queue is FULL, the producer is REJECTED (or would
block) rather than piling up unbounded work. This is backpressure -- bounding
load at the source.
"""

from collections import deque  # => deque: a bounded FIFO queue
from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-31: a bounded queue + a slow consumer
class BoundedQueue:
    capacity: int  # => the max items allowed in-flight
    queue: deque[int] = field(default_factory=deque[int])  # => the bounded buffer
    rejected: list[int] = field(default_factory=list[int])  # => items turned away when full
    processed: list[int] = field(default_factory=list[int])  # => items the consumer finished

    def try_produce(self, item: int) -> bool:  # => co-31: enqueue only if room remains
        if len(self.queue) >= self.capacity:  # => co-31: FULL -> reject (backpressure on the producer)
            self.rejected.append(item)  # => record the rejected item
            return False  # => producer must slow down / retry
        self.queue.append(item)  # => enqueued
        return True  # => accepted

    def consume_one(self) -> int | None:  # => the slow consumer finishes one item
        if not self.queue:  # => nothing in-flight
            return None  # => idle
        item = self.queue.popleft()  # => take the front item
        self.processed.append(item)  # => finished
        return item  # => the item consumed


q = BoundedQueue(capacity=2)  # => co-31: only 2 items may be in-flight at once

# A fast producer floods 4 items; only 2 fit, 2 are rejected (backpressure).
produced = [q.try_produce(i) for i in range(1, 5)]  # => items 1,2 accepted; 3,4 rejected
print(f"produced results: {produced}")  # => Output: [True, True, False, False]
print(f"rejected (backpressure): {q.rejected}")  # => Output: [3, 4]
print(f"in-flight: {list(q.queue)}")  # => Output: [1, 2]

# The consumer drains one item, freeing a slot -- the producer may now retry one.
q.consume_one()  # => item 1 finished -> a slot opens
retry = q.try_produce(3)  # => co-31: now there is room -> accepted
print(f"retry item 3 after a slot freed: {retry}, in-flight: {list(q.queue)}")  # => Output: True, [2, 3]

assert produced == [True, True, False, False]  # => co-31: the producer was rejected when full
assert retry is True  # => co-31: backpressure lifts once a slot frees

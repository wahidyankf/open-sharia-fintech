"""Example 7: Queue with collections.deque."""

# deque supports O(1) operations at BOTH ends -- ideal for a FIFO queue (co-05, co-06).
from collections import deque

queue: deque[str] = deque()  # => queue starts empty
queue.append("first")  # => enqueue at the right end -- queue is ["first"]
queue.append("second")  # => enqueue at the right end -- queue is ["first", "second"]
queue.append("third")  # => enqueue -- queue is ["first", "second", "third"]

served = queue.popleft()  # => dequeue from the LEFT end -- First-In-First-Out (FIFO)
# => served is "first"; queue becomes deque(["second", "third"]), both O(1)
print(served)  # => Output: first
print(list(queue))  # => Output: ['second', 'third']

assert served == "first"  # => confirms the earliest-enqueued item served first
assert list(queue) == ["second", "third"]  # => confirms FIFO order for the rest
print("ex-07 OK")  # => Output: ex-07 OK

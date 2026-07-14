"""Example 8: Deque Operations at Both Ends."""

# A deque is a double-ended queue: push/pop at EITHER end, all O(1) (co-06).
from collections import deque  # => imports the stdlib double-ended queue type

items: deque[int] = deque([2, 3])  # => items starts as deque([2, 3])
items.appendleft(1)  # => pushes 1 onto the LEFT end -- items is [1, 2, 3]
items.append(4)  # => pushes 4 onto the RIGHT end -- items is [1, 2, 3, 4]
print(list(items))  # => Output: [1, 2, 3, 4]

right = items.pop()  # => pops from the RIGHT end -- right is 4, items is [1, 2, 3]
left = items.popleft()  # => pops from the LEFT end -- left is 1, items is [2, 3]
print(right, left)  # => Output: 4 1
print(list(items))  # => Output: [2, 3]

assert right == 4  # => confirms pop() removed the rightmost element
assert left == 1  # => confirms popleft() removed the leftmost element
assert list(items) == [2, 3]  # => confirms the middle elements survive both pops
print("ex-08 OK")  # => Output: ex-08 OK

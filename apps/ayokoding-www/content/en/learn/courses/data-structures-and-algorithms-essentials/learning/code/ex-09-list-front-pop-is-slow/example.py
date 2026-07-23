"""Example 9: list.pop(0) vs deque.popleft -- Same Result, Different Cost."""

# Both dequeue "the first item," but list.pop(0) is O(n) -- it must shift every
# remaining element left by one -- while deque.popleft is O(1) (co-05, co-01).
from collections import deque

as_list: list[str] = ["a", "b", "c"]
as_deque: deque[str] = deque(["a", "b", "c"])

list_result = as_list.pop(0)  # => O(n): shifts "b" and "c" left one slot each
# => as_list is now ["b", "c"] -- correct, but does O(n) work for ONE dequeue
deque_result = as_deque.popleft()  # => O(1): just moves an internal head pointer
# => as_deque is now deque(["b", "c"]) -- same logical result, O(1) work
print(list_result, deque_result)  # => Output: a a
print(as_list, list(as_deque))  # => Output: ['b', 'c'] ['b', 'c']

assert list_result == deque_result == "a"  # => confirms identical dequeued values
assert as_list == list(as_deque) == ["b", "c"]  # => confirms identical final order
print("ex-09 OK")  # => Output: ex-09 OK

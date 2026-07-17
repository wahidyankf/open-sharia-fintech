"""Example 9: heapq Push and Pop -- Smallest Always Emerges First."""

# heapq maintains the MIN-HEAP property directly on a plain list (co-09): the
# smallest element is always at index 0, and heappush/heappop keep that
# property true in O(log n) each, without ever fully sorting the list.
import heapq  # => the stdlib binary-heap module -- operates in place on a list

heap: list[int] = []  # => starts as an empty heap -- just an empty list
for value in [
    5,
    1,
    8,
    3,
    9,
    2,
]:  # => pushes in a deliberately unsorted order
    heapq.heappush(heap, value)  # => O(log n): sift the new value up to its spot
    print(f"after push {value}: heap[0]={heap[0]}")  # => Output: current heap minimum
    # => the SMALLEST value pushed so far is always at heap[0] after every push

popped_order: list[int] = []  # => records the order values come out in
while heap:  # => drains the heap one minimum at a time
    smallest = heapq.heappop(heap)  # => O(log n): remove and return the current minimum
    popped_order.append(smallest)  # => records this pop for the assertion below
print(popped_order)  # => Output: [1, 2, 3, 5, 8, 9]

assert popped_order == [
    1,
    2,
    3,
    5,
    8,
    9,
]  # => confirms values emerge in ascending order, though pushed unsorted
assert popped_order == sorted(
    popped_order
)  # => a heap-drain is ALWAYS a sorted sequence
print("ex-09 OK")  # => Output: ex-09 OK

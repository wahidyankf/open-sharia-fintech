"""Example 9: heapq Push and Pop -- Smallest Always Emerges First."""

# heapq maintains the MIN-HEAP property directly on a plain list (co-09): the
# smallest element is always at index 0, and heappush/heappop keep that
# property true in O(log n) each, without ever fully sorting the list.
import heapq  # => the stdlib binary-heap module -- operates in place on a list

heap: list[int] = []  # => starts as an empty heap -- just an empty list
for value in [
    5,  # => first push -- becomes heap[0] until something smaller arrives
    1,  # => new minimum -- heapq sifts it up to heap[0] in O(log n)
    8,  # => larger than the current minimum -- sinks below heap[0]
    3,  # => smaller than 8 but not smaller than 1 -- stays below heap[0]
    9,  # => the largest value pushed so far -- sinks to a leaf position
    2,  # => second-smallest overall -- settles near, but not at, the root
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
    1,  # => smallest pushed value -- must pop first
    2,  # => second-smallest -- pops right after 1
    3,  # => third-smallest in the drain order
    5,  # => fourth -- the original first-pushed value, now mid-order
    8,  # => fifth -- was pushed early but is large
    9,  # => largest pushed value -- must pop last
]  # => confirms values emerge in ascending order, though pushed unsorted
assert popped_order == sorted(
    popped_order  # => re-sorting an already-sorted list is a no-op if the drain worked
)  # => a heap-drain is ALWAYS a sorted sequence
print("ex-09 OK")  # => Output: ex-09 OK

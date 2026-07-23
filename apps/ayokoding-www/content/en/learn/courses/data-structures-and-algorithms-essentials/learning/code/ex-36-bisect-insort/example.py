"""Example 36: bisect.insort -- Insert While Staying Sorted."""

# insort finds the sorted position (O(log n) search) then inserts (O(n) shift) --
# cheaper than appending and re-sorting the whole list every time (co-14, co-03).
import bisect

sorted_values: list[int] = [1, 3, 5, 9]  # => already sorted ascending
bisect.insort(sorted_values, 7)  # => inserts 7 at the position that keeps order intact
print(sorted_values)  # => Output: [1, 3, 5, 7, 9]

assert sorted_values == [
    1,
    3,
    5,
    7,
    9,
]  # => confirms the list stayed sorted after insert
assert sorted_values == sorted(sorted_values)  # => cross-checks against sorted() itself
print("ex-36 OK")  # => Output: ex-36 OK

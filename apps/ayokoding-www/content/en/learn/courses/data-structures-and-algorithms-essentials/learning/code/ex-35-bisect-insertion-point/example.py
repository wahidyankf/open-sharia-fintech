"""Example 35: bisect.bisect_left -- Sorted Insertion Point."""

# bisect_left finds WHERE a value would go to keep the list sorted, in O(log n),
# without actually inserting it -- the stdlib's binary search, ready-made (co-14).
import bisect

sorted_values: list[int] = [1, 3, 5, 7, 9]  # => must already be sorted
point_for_present = bisect.bisect_left(
    sorted_values, 5
)  # => 5 already exists at index 2
point_for_absent = bisect.bisect_left(sorted_values, 6)  # => 6 belongs between 5 and 7
print(point_for_present)  # => Output: 2
print(point_for_absent)  # => Output: 3

assert (
    point_for_present == 2
)  # => confirms bisect_left lands ON an existing equal value
assert point_for_absent == 3  # => confirms the insertion index for a missing value
print("ex-35 OK")  # => Output: ex-35 OK

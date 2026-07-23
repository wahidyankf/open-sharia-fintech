"""Example 32: Binary Search -- Value Not Found."""


# Same halving search as Example 31; -1 signals "absent" (co-14).
def binary_search(
    items: list[int], target: int
) -> int:  # => a plain iterative function
    low, high = 0, len(items) - 1  # => the inclusive range still being searched
    while low <= high:  # => O(log n): the range shrinks by half every iteration
        mid = (low + high) // 2  # => the midpoint of the current range
        if items[mid] == target:  # => not true anywhere in this fixture
            return mid  # => not reached in this example
        if items[mid] < target:  # => the midpoint is too small
            low = mid + 1  # => target must be in the RIGHT half -- discard the left
        else:  # => the midpoint is too large
            high = mid - 1  # => target must be in the LEFT half -- discard the right
    return -1  # => low crosses high with no match -- the range is now empty


sorted_values = [1, 3, 5, 7, 9, 11, 13]  # => the same sorted list as Example 31
index = binary_search(
    sorted_values, 6
)  # => 6 is not present -- it would sit between 5 and 7
print(index)  # => Output: -1

assert (
    index == -1
)  # => confirms a missing value returns the sentinel, not a wrong index
assert 6 not in sorted_values  # => confirms the target really is absent from the source
print("ex-32 OK")  # => Output: ex-32 OK

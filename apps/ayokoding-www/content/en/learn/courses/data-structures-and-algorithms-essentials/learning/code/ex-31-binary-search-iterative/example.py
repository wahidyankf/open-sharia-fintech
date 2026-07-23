"""Example 31: Iterative Binary Search."""


# Halves the candidate range each step -- requires a SORTED input, O(log n) (co-14).
def binary_search(
    items: list[int], target: int
) -> int:  # => a plain iterative function
    low, high = 0, len(items) - 1  # => the inclusive range still being searched
    while low <= high:  # => keeps narrowing until the range is empty
        mid = (low + high) // 2  # => the midpoint of the current range
        if items[mid] == target:  # => a direct hit at the midpoint
            return mid  # => found -- return immediately, no more halving needed
        if items[mid] < target:  # => the midpoint is too small
            low = mid + 1  # => target must be in the RIGHT half -- discard the left
        else:  # => the midpoint is too large
            high = mid - 1  # => target must be in the LEFT half -- discard the right
    return -1  # => range emptied out with no match


sorted_values = [1, 3, 5, 7, 9, 11, 13]  # => MUST be sorted for binary search to work
index = binary_search(sorted_values, 9)  # => 9 sits at index 4
print(index)  # => Output: 4

assert index == 4  # => confirms the returned index matches sorted_values[4]
assert sorted_values[index] == 9  # => confirms indexing back recovers the target
print("ex-31 OK")  # => Output: ex-31 OK

"""Example 16: Linear Search -- Value Not Found."""


# Scans items left to right; -1 signals "never found" (co-13).
def linear_search(items: list[int], target: int) -> int:  # => same shape as Example 15
    for index, value in enumerate(items):  # => must check EVERY element on a miss
        if value == target:  # => not true for any element in this fixture
            return index  # => not reached in this example -- target is absent
    return -1  # => the whole list was scanned with no match -- worst case O(n)


numbers = [8, 3, 5, 1, 9, 2]  # => the same list as Example 15, searched for 42
missing_index = linear_search(numbers, 42)  # => 42 is not in numbers at all
print(missing_index)  # => Output: -1

assert missing_index == -1  # => confirms the sentinel value signals "not found"
assert 42 not in numbers  # => confirms the target really is absent from the source
print("ex-16 OK")  # => Output: ex-16 OK

"""Example 1: List Append and Index."""

# A dynamic array literal -- Python's list grows/shrinks in place (co-03).
numbers: list[int] = [10, 20, 30]  # => numbers is [10, 20, 30], length 3
numbers.append(40)  # => grows the array by one -- amortized O(1) (co-02)
# => no full copy happens on THIS call; CPython over-allocates spare
# => capacity so most appends just write into already-reserved space
print(len(numbers))  # => Output: 4
print(numbers[0])  # => index 0 is O(1): direct offset math -- Output: 10
print(numbers[-1])  # => negative index counts from the end -- Output: 40

assert len(numbers) == 4  # => confirms the append grew the list by one
assert numbers[0] == 10  # => confirms the first element is unchanged
assert numbers[-1] == 40  # => confirms the appended value is now last
print("ex-01 OK")  # => Output: ex-01 OK

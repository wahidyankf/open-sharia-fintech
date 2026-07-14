"""Example 2: List Slicing."""

# lst[start:stop] returns a NEW list -- Python's list stores contiguously (co-03).
letters: list[str] = ["a", "b", "c", "d", "e"]  # => letters has 5 elements, index 0..4
middle = letters[1:4]  # => copies index 1 up to (not including) 4
# => middle is ["b", "c", "d"] -- a fresh list, not a view into letters
tail = letters[3:]  # => omitting stop means "through the end"
print(middle)  # => Output: ['b', 'c', 'd']
print(tail)  # => Output: ['d', 'e']

assert middle == ["b", "c", "d"]  # => confirms the sub-list matches the expected slice
assert tail == ["d", "e"]  # => confirms the open-ended slice reached the last element
assert letters == [
    "a",
    "b",
    "c",
    "d",
    "e",
]  # => confirms slicing never mutates the source
print("ex-02 OK")  # => Output: ex-02 OK

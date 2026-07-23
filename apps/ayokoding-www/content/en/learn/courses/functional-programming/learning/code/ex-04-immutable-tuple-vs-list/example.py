"""Example 4: Tuple Immutability vs. List Mutability."""

mutable_list: list[int] = [
    1,
    2,
    3,
]  # => a list -- mutable, in-place assignment is legal
mutable_list[0] = 99  # => legal: lists allow item assignment
print(mutable_list)  # => Output: [99, 2, 3]

immutable_tuple: tuple[int, int, int] = (
    1,
    2,
    3,
)  # => a tuple -- immutable, fixed after creation
try:  # => opens a block that expects the next line to raise
    immutable_tuple[0] = 99  # type: ignore[index]  # => attempts item assignment on a tuple
    raised = False  # => unreachable if TypeError fires, kept for completeness
except TypeError as exc:  # => tuples have no __setitem__ -- this is EXPECTED, not a bug
    raised = True  # => confirms the immutability guarantee was actually enforced
    print(f"raised: {type(exc).__name__}")  # => Output: raised: TypeError

print(raised)  # => Output: True
print(
    immutable_tuple
)  # => Output: (1, 2, 3) -- unchanged, the assignment never happened

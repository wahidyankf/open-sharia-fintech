"""Example 5: Stack with Push and Pop."""

# A list used as a stack: append() pushes, pop() pops -- both O(1) at the end (co-04).
stack: list[str] = []  # => stack starts empty
stack.append("first")  # => pushes "first" -- stack is ["first"]
stack.append("second")  # => pushes "second" -- stack is ["first", "second"]
stack.append("third")  # => pushes "third" -- stack is ["first", "second", "third"]

top = stack.pop()  # => pops the LAST pushed item -- Last-In-First-Out (LIFO)
# => top is "third"; stack shrinks back to ["first", "second"]
print(top)  # => Output: third
print(stack)  # => Output: ['first', 'second']

assert top == "third"  # => confirms the most recently pushed item popped first
assert stack == ["first", "second"]  # => confirms the remaining order is unchanged
assert stack.pop() == "second"  # => confirms the next pop follows LIFO order too
print("ex-05 OK")  # => Output: ex-05 OK

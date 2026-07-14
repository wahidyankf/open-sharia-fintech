"""Example 16: Tuple Unpacking."""

pair: tuple[int, int] = (10, 20)  # => a fixed-size, immutable sequence literal
x, y = pair  # => unpacks pair's two elements into x and y in one statement
print(x, y)  # => Output: 10 20

"""Example 52: Read Text File."""

with open("data.txt") as f:  # => `with` guarantees the file closes, even on error
    print(f.read(), end="")  # => .read() returns the WHOLE file as one string
# => Output: line1<newline>line2<newline>

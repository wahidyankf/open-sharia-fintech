"""Example 54: Append File."""

# Each `with` block closes its file automatically when the block exits.
with open("log.txt", "w") as f:  # => "w" starts the file fresh, discarding old content
    f.write("first\n")  # => writes the first line to log.txt

with open("log.txt", "a") as f:  # => "a" appends -- prior content is kept
    f.write("second\n")  # => appends a second line after "first\n"

with open("log.txt") as f:  # => default mode "r" opens the file for reading
    print(f.read(), end="")  # => Output: first<newline>second<newline>

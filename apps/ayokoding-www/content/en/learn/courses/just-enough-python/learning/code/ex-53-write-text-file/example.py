"""Example 53: Write Text File."""

with open("out.txt", "w") as f:  # => "w" truncates the file, then opens it for writing
    f.write("line1\n")  # => .write() does NOT add a newline automatically
    f.write("line2\n")

with open("out.txt") as f:  # => a fresh `with`, reading back what was just written
    print(repr(f.read()))  # => repr() shows the embedded \n characters explicitly
# => Output: 'line1\nline2\n'

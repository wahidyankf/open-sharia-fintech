"""Example 48: try/except."""

# try/except lets the program continue after an exception instead of crashing.
try:  # => wraps the risky operation so we can catch its exception
    1 / 0  # => integer division by zero raises ZeroDivisionError
except ZeroDivisionError:  # => catches exactly that exception type, nothing else
    print("cannot divide")  # => Output: cannot divide

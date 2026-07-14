"""Example 33: Generator Expression."""

# No brackets -- values are produced lazily, one at a time, for sum().
total: int = sum(n * n for n in range(4))
print(total)  # => 0+1+4+9 -- Output: 14

"""Example 26: for + range."""

# range(start, stop) is a lazy sequence -- stop is never included.
total: int = 0  # => total is 0 (type: int) -- the running-sum accumulator
for n in range(1, 6):  # => range(1, 6) yields 1, 2, 3, 4, 5 -- stop is exclusive
    total += n  # => accumulates a running sum across the loop
print(total)  # => 1+2+3+4+5 -- Output: 15

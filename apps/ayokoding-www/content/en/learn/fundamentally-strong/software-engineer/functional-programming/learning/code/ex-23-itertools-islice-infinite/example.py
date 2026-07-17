"""Example 23: islice Over an Infinite count()."""

from itertools import (
    count,
    islice,
)  # => count(): an infinite counter; islice: a lazy slice

infinite_evens = (n for n in count(0, 2))  # => LAZY, infinite: 0, 2, 4, 6, ... forever
first_five = list(
    islice(infinite_evens, 5)
)  # => islice pulls exactly 5 values, then STOPS
# => the underlying infinite generator is NEVER exhausted -- islice just stops pulling

print(first_five)  # => Output: [0, 2, 4, 6, 8]
print(
    len(first_five)
)  # => Output: 5 -- islice never tries to exhaust the infinite source
next_value = next(
    infinite_evens
)  # => the underlying generator resumes right where islice left it
print(
    next_value
)  # => Output: 10 -- confirms islice consumed exactly the first 5, no more

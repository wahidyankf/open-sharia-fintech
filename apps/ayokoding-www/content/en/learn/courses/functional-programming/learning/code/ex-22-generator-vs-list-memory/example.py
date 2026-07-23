"""Example 22: Generator Expression vs. List."""

import sys  # => sys.getsizeof measures the actual object footprint, in bytes

n = 1_000_000  # => a large N -- big enough to make the memory difference obvious

eager_list = [
    i * i for i in range(n)
]  # => EAGER: every single square computed and stored NOW
lazy_generator = (
    i * i for i in range(n)
)  # => LAZY: builds a generator object, computes NOTHING yet
# => same source expression, two entirely different memory strategies

list_bytes = sys.getsizeof(
    eager_list
)  # => size of N already-materialized integers' container
generator_bytes = sys.getsizeof(
    lazy_generator
)  # => size of the generator machinery only

print(
    list_bytes > generator_bytes
)  # => Output: True -- the list is dramatically larger
print(
    generator_bytes < 300
)  # => Output: True -- a generator's footprint stays tiny regardless of n
print(
    next(lazy_generator)
)  # => Output: 0 -- the FIRST square is only computed on this pull

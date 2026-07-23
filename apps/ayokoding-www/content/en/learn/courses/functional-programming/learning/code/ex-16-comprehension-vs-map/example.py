"""Example 16: A Comprehension Matching map() and filter()."""

nums = [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
]  # => the shared source sequence for both approaches

via_map_filter = (
    list(  # => map(square, filter(is_even, nums)), spelled out with a lambda
        map(
            lambda n: n * n, filter(lambda n: n % 2 == 0, nums)
        )  # => two nested lazy iterators
    )
)  # => filter runs first (keeps evens), THEN map squares what survived

via_comprehension = [
    n * n for n in nums if n % 2 == 0
]  # => same two steps, ONE expression
# => "if n % 2 == 0" is the filter step; "n * n" is the map step -- read left to right

print(via_map_filter)  # => Output: [4, 16, 36, 64, 100]
print(via_comprehension)  # => Output: [4, 16, 36, 64, 100]
print(
    via_map_filter == via_comprehension
)  # => Output: True -- two spellings, identical result

"""Example 28: enumerate + zip."""

# enumerate pairs each element with its index, starting from 0.
for index, letter in enumerate(["a", "b"]):
    print(index, letter)  # => Output: 0 a, then 1 b

# zip pairs elements positionally; it stops at the shortest input.
for number, letter in zip([1, 2], ["x", "y"]):
    print(number, letter)  # => Output: 1 x, then 2 y

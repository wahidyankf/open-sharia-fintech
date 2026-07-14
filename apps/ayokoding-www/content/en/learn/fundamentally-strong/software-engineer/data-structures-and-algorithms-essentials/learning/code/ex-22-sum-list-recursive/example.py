"""Example 22: Recursively Sum a List."""


# Sums values by adding its head to the sum of its tail (co-17).
def sum_list(values: list[int]) -> int:  # => a plain recursive function
    if not values:  # => BASE CASE -- an empty list sums to 0
        return 0  # => the additive identity, so the recursion can bottom out
    return values[0] + sum_list(values[1:])  # => RECURSIVE CASE: head + sum(tail)
    # => values[1:] copies a shrinking slice each call -- fine for small lists


total = sum_list([1, 2, 3, 4, 5])  # => 1+(2+(3+(4+(5+0)))) -- five nested calls
print(total)  # => Output: 15

assert total == 15  # => confirms the recursive total matches the expected sum
assert sum_list([]) == 0  # => confirms the base case alone returns correctly
print("ex-22 OK")  # => Output: ex-22 OK

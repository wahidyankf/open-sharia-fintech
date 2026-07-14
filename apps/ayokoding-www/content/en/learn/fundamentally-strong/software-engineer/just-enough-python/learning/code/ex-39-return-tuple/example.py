"""Example 39: Return Tuple."""


# Returns a 2-tuple of (quotient, remainder).
def divide(a: int, b: int) -> tuple[int, int]:
    return a // b, a % b  # => a bare comma builds a tuple -- two values, one return


# Tuple unpacking assigns each returned value to a name, in order.
quotient, remainder = divide(10, 3)  # => unpacks the returned tuple into two names
print(quotient, remainder)  # => 10 // 3 = 3, 10 % 3 = 1 -- Output: 3 1

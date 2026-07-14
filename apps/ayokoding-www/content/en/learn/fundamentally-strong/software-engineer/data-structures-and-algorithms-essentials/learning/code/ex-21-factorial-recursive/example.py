"""Example 21: Recursive Factorial."""


# Computes n! by expressing it in terms of a smaller instance (co-17).
def factorial(n: int) -> int:  # => a plain recursive function
    if n == 0:  # => the BASE CASE -- stops the recursion from going forever
        return 1  # => 0! is defined as 1 by convention
    return n * factorial(n - 1)  # => the RECURSIVE CASE -- n! = n * (n-1)!
    # => each call consumes one call-stack frame until n reaches 0


result = factorial(5)  # => 5*4*3*2*1*1 -- five nested calls, then unwinds
print(result)  # => Output: 120

assert result == 120  # => confirms factorial(5) matches the known value
assert factorial(0) == 1  # => confirms the base case itself returns correctly
print("ex-21 OK")  # => Output: ex-21 OK

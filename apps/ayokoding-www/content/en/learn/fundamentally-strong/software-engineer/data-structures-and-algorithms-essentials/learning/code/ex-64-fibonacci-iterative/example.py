"""Example 64: Bottom-Up Iterative Fibonacci."""


# Builds up from fib(0), fib(1) with two rolling variables -- O(n) time, O(1) space (co-18).
def fib(n: int) -> int:  # => a plain iterative function, no recursion at all
    previous, current = (
        0,
        1,
    )  # => previous=fib(0), current=fib(1) -- no cache dict needed
    for _ in range(
        n
    ):  # => exactly n iterations -- no repeated subproblems exist here at all
        previous, current = (
            current,
            previous + current,
        )  # => slides the window forward by one
        # => this single line replaces BOTH Example 61's recursion tree and Example 62's cache
    return previous  # => after n slides, previous holds fib(n)


result = fib(10)  # => same correct answer as Examples 61-63, with O(1) extra space
print(result)  # => Output: 55

assert result == 55  # => confirms the iterative version matches the recursive versions
assert (
    fib(0) == 0 and fib(1) == 1
)  # => confirms both base cases hold under the iterative form
print("ex-64 OK")  # => Output: ex-64 OK

"""Example 61: Naive Recursive Fibonacci -- and Its Exponential Cost."""

call_count = 0  # => module-level counter, incremented on every call


# fib(n) = fib(n-1) + fib(n-2) -- but RECOMPUTES overlapping subproblems (co-17, co-01).
def fib(n: int) -> int:  # => a plain recursive function, no caching at all
    global call_count  # => allows this function to mutate the module-level counter
    call_count += 1  # => tallies every single call, including duplicates
    if n <= 1:  # => BASE CASE -- fib(0)=0, fib(1)=1
        return n  # => n itself is the answer for 0 and 1
    return fib(n - 1) + fib(
        n - 2
    )  # => two RECURSIVE calls -- the tree branches exponentially
    # => fib(n-2) gets recomputed from scratch inside BOTH fib(n-1) and fib(n) itself


result = fib(10)  # => the correct value, but at exponential O(2^n) call-count cost
print(result)  # => Output: 55
print(
    call_count
)  # => Output: 177 (far more than the 10 "useful" subproblems that exist)

assert result == 55  # => confirms fib(10) matches the known correct value
assert call_count > 10  # => confirms wasteful REPEATED work: way more calls than n
print("ex-61 OK")  # => Output: ex-61 OK

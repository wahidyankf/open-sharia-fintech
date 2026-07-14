"""Example 62: Memoized Fibonacci with a Dict Cache."""

call_count = 0  # => tallies every call, same as Example 61, for a fair comparison
cache: dict[int, int] = {}  # => maps n -> fib(n), once computed (co-19, co-08)


# Same recurrence as Example 61, but a dict CACHE collapses repeat work (co-19).
def fib(n: int) -> int:  # => a recursive function with a memoization cache
    global call_count  # => allows this function to mutate the module-level counter
    call_count += 1  # => tallies every call, including cache hits
    if n in cache:  # => O(1) average lookup -- this subproblem was already solved
        return cache[n]  # => reuse the stored answer -- no further recursion needed
    if n <= 1:  # => BASE CASE
        result = n  # => n itself is the answer for 0 and 1
    else:  # => RECURSIVE CASE, but each n computed ONCE
        result = fib(n - 1) + fib(
            n - 2
        )  # => combines two smaller cached-or-computed results
    cache[n] = result  # => store BEFORE returning, so future calls hit the cache
    return result  # => the (now cached) answer for this n


result = fib(10)  # => same correct answer as the naive version
print(result)  # => Output: 55
print(call_count)  # => Output: 19 (linear in n, not exponential)

assert result == 55  # => confirms memoization doesn't change the correct answer
assert call_count < 30  # => confirms FAR fewer calls than Example 61's 177
print("ex-62 OK")  # => Output: ex-62 OK

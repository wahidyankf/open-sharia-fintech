"""Example 23: Countdown -- Iterative vs Recursive, Same Output."""


# Builds [n, n-1, ..., 1] with an explicit loop -- no extra call-stack frames (co-18).
def countdown_iterative(n: int) -> list[int]:  # => the iterative version
    result: list[int] = []  # => grows one item per loop iteration
    while n > 0:  # => loops until n reaches 0 -- state lives in a local variable
        result.append(n)  # => records the current count
        n -= 1  # => advances the loop's own state, no recursive call needed
    return result  # => the finished countdown list


# Builds the same list by recursing -- one call-stack frame per step (co-17, co-18).
def countdown_recursive(n: int) -> list[int]:  # => the recursive version
    if n == 0:  # => BASE CASE: nothing left to count down
        return []  # => an empty list -- recursion bottoms out here
    return [n] + countdown_recursive(
        n - 1
    )  # => RECURSIVE CASE: prepend n, recurse smaller


iterative_result = countdown_iterative(4)  # => [4, 3, 2, 1] via a while loop
recursive_result = countdown_recursive(4)  # => [4, 3, 2, 1] via recursive calls
print(iterative_result)  # => Output: [4, 3, 2, 1]
print(recursive_result)  # => Output: [4, 3, 2, 1]

assert (
    iterative_result == recursive_result == [4, 3, 2, 1]
)  # => confirms identical results
print("ex-23 OK")  # => Output: ex-23 OK

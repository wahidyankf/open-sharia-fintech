"""Example 66: A Trampoline Simulating Tail-Call Optimization."""

from typing import (
    Callable,
)  # => Callable types the zero-arg thunk; "Bounce | int" uses PEP 604 union syntax


class Bounce:  # => a marker: "not done yet, call this thunk next" -- NOT the final answer
    def __init__(
        self, thunk: Callable[[], "Bounce | int"]
    ) -> None:  # => wraps a zero-arg step function
        self.thunk = (
            thunk  # => stored for the trampoline loop to call on its NEXT iteration
        )


def trampoline(
    result: "Bounce | int",
) -> int:  # => drives the loop -- ONE stack frame, however deep
    while isinstance(
        result, Bounce
    ):  # => keeps bouncing as long as we get another Bounce back
        result = (
            result.thunk()
        )  # => calls the next step -- reuses THIS loop's frame, not a new one
    return result  # => once it's a plain int, the computation is actually done


def sum_to_n_trampolined(
    n: int, acc: int = 0
) -> "Bounce | int":  # => "recursive-looking" but returns a Bounce
    if n == 0:  # => base case: nothing left to add
        return acc  # => a plain int, stops the trampoline
    return Bounce(
        lambda: sum_to_n_trampolined(n - 1, acc + n)
    )  # => NOT a real recursive call -- returns immediately


deep_n = 50_000  # => far past CPython's default recursion limit if called naively

result = trampoline(
    sum_to_n_trampolined(deep_n)
)  # => the WHILE LOOP does the "recursion," not the call stack

# => the trampoline pattern is Python's manual workaround for missing tail-call optimization
print(result)  # => Output: 1250025000
print(
    result == deep_n * (deep_n + 1) // 2
)  # => Output: True -- correct despite the extreme depth

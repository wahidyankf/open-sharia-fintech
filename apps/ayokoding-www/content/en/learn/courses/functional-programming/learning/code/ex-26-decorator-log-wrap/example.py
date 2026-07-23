"""Example 26: A Logging Decorator Wraps a Function."""

from typing import (
    Callable,
)  # => the type shape both the wrapped and wrapper functions share

calls: list[str] = []  # => records what the decorator observed, for verification below


def log_calls(
    fn: Callable[[int, int], int],
) -> Callable[[int, int], int]:  # => decorator: fn -> wrapped fn
    def wrapper(
        a: int, b: int
    ) -> int:  # => runs INSTEAD of fn when the decorated name is called
        calls.append(f"calling {fn.__name__}({a}, {b})")  # => logs BEFORE the real call
        result = fn(a, b)  # => delegates to the original, undecorated function
        calls.append(
            f"{fn.__name__} returned {result}"
        )  # => logs AFTER, using the real result
        return result  # => the wrapper's return value is EXACTLY the original's return value

    return wrapper  # => this function object replaces add everywhere add() is called


@log_calls  # => equivalent to: add = log_calls(add)
def add(a: int, b: int) -> int:  # => the plain function BEFORE decoration wraps it
    return a + b  # => the ordinary, undecorated computation


wrapped_result = add(2, 3)  # => actually calls wrapper(2, 3), which logs then delegates
print(
    wrapped_result
)  # => Output: 5 -- the wrapped result is unchanged from the plain call
print(calls)  # => Output: ['calling add(2, 3)', 'add returned 5']

"""Example 62: A @curry Decorator Auto-Currying by Arity."""

import inspect  # => inspects fn's own signature to learn how many arguments it needs
from functools import wraps  # => preserves add3's identity through the decorator
from typing import (
    Any,
    Callable,
)  # => Any/Callable type this deliberately dynamic decorator


def curry(
    fn: Callable[..., Any],
) -> Callable[..., Any]:  # => a decorator that auto-curries fn
    arity = len(
        inspect.signature(fn).parameters
    )  # => how many arguments fn ultimately needs

    @wraps(fn)  # => preserves fn's __name__/__doc__ on the curried wrapper
    def curried(*args: Any) -> Any:  # => accumulates arguments across MULTIPLE calls
        if (
            len(args) >= arity
        ):  # => enough arguments collected -- call the real function NOW
            return fn(*args)  # => the real call, with every argument finally in hand

        def more_needed(
            *more: Any,
        ) -> Any:  # => named + fully typed -- an untyped lambda can't carry annotations
            return curried(
                *args, *more
            )  # => not enough yet -- keeps accumulating arguments

        return more_needed  # => returns the function wanting more arguments

    return curried  # => curry itself returns the auto-currying wrapper


@curry  # => wraps add3 so it can be called one argument at a time, or all at once
def add3(a: int, b: int, c: int) -> int:  # => an ordinary 3-argument function
    return a + b + c  # => the actual sum


all_at_once = add3(
    1, 2, 3
)  # => calling with all 3 arguments works like the undecorated function
one_at_a_time = add3(1)(2)(
    3
)  # => calling one argument per call ALSO reaches the same result
mixed = add3(1, 2)(3)  # => and any grouping in between works too

# => auto-currying via inspect.signature makes ANY function callable one argument at a time
print(all_at_once)  # => Output: 6
print(one_at_a_time)  # => Output: 6
print(mixed)  # => Output: 6

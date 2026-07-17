"""Example 73: A Small Point-Free Combinator Library."""

from functools import reduce  # => reduce powers pipe's left-to-right fold
from typing import (
    Any,
    Callable,
    TypeVar,
)  # => Callable/TypeVar type this small combinator library; Any types pipe's dynamic arity

A = TypeVar("A")  # => a generic type parameter shared by const
B = TypeVar("B")  # => a second generic type parameter shared by flip


def pipe(
    *fns: Callable[..., Any],
) -> Callable[..., Any]:  # => LEFT-to-right composition -- the first fn runs FIRST
    def apply_step(
        acc: Any, fn: Callable[..., Any]
    ) -> Any:  # => named + typed -- one fold step, calls fn on acc
        return fn(
            acc
        )  # => applies ONE fn to the running accumulator, returns the next accumulator

    def piped(
        x: Any,
    ) -> Any:  # => named + typed -- an untyped lambda can't carry these annotations
        return reduce(apply_step, fns, x)  # => folds fns in ORDER, unlike compose

    return piped  # => pipe itself returns the composed pipeline function


def const(
    value: A,
) -> Callable[..., A]:  # => a combinator: ignores its argument(s), always returns value
    return lambda *_ignored: (
        value
    )  # => the returned function discards WHATEVER it's called with


def flip(
    fn: Callable[[A, B], A],
) -> Callable[[B, A], A]:  # => a combinator: swaps a 2-arg function's order
    return lambda b, a: fn(a, b)  # => calls fn with its two arguments REVERSED


def subtract(
    a: int, b: int
) -> int:  # => an ordinary 2-argument function, order matters
    return a - b  # => the actual subtraction


always_zero = const(0)  # => a function of ANY arguments that always returns 0
flipped_subtract = flip(subtract)  # => subtract with its arguments swapped


def add_one(
    x: int,
) -> (
    int
):  # => named + typed -- pipe's Callable[..., Any] gives lambdas no param context
    return x + 1  # => adds 1 to x -- one plain step for pipe/flip to compose over


def double(x: int) -> int:  # => named + typed, same reasoning
    return x * 2  # => doubles x -- the second plain step in the transform pipeline


transform = pipe(
    add_one, double, str
)  # => a combined "add 1, double, stringify" pipeline

# => a tiny combinator library is how point-free style scales beyond one-off rewrites
print(transform(3))  # => Output: 8  (str of (3+1)*2)
print(always_zero(1, 2, 3))  # => Output: 0 -- ignores every argument it was given
print(subtract(10, 3))  # => Output: 7
print(
    flipped_subtract(10, 3)
)  # => Output: -7 -- same two arguments, swapped order changes the answer

"""Example 72: Left-Identity, Right-Identity, and Associativity for Result."""

from __future__ import (
    annotations,
)  # => enables the quoted 'Result[U, object]' forward references below

from dataclasses import (
    dataclass,
)  # => @dataclass(frozen=True) builds both Result variants
from typing import (
    Callable,
    Generic,
    TypeVar,
)  # => Generic/TypeVar/Callable type bind and unit below

T = TypeVar("T")  # => the type of the value an Ok wraps
U = TypeVar("U")  # => the type bind's step function returns
E = TypeVar("E")  # => the type of the error an Err wraps
F = TypeVar(
    "F"
)  # => the error type threaded through bind's step function, not hardcoded to object


@dataclass(frozen=True)  # => marks Ok immutable, matching the FP style
class Ok(Generic[T]):  # => the class body begins here
    value: T  # => the single field this variant carries

    def bind(
        self, fn: Callable[[T], "Result[U, F]"]
    ) -> "Result[U, F]":  # => F comes from fn's OWN error type
        return fn(
            self.value
        )  # => unwraps, runs fn (which itself returns a Result), no double-wrap


@dataclass(frozen=True)  # => marks Err immutable too
class Err(Generic[E]):  # => the class body begins here
    error: E  # => the single field this variant carries

    def bind(
        self, fn: Callable[[T], U]
    ) -> "Err[E]":  # => NO-OP, generic so a typed fn still passes the check
        return self  # => fn never runs once the chain has already failed


Result = Ok[T] | Err[E]  # => the ADT itself: a Result is EITHER variant


def unit(
    x: T,
) -> (
    "Result[T, object]"
):  # => the monad's "wrap a plain value" operation, a.k.a. return/pure
    return Ok(x)  # => the simplest possible success


def half(
    n: int,
) -> "Result[float, str]":  # => an arbitrary bind step, reused by all three law checks
    return (
        Ok(n / 2) if n % 2 == 0 else Err(f"{n} is odd")
    )  # => succeeds on even n, fails on odd n


def add_ten(
    x: float,
) -> "Result[float, str]":  # => a SECOND arbitrary bind step, for associativity
    return Ok(x + 10)  # => always succeeds


left_identity_holds = unit(8).bind(half) == half(8)  # => unit(x).bind(f) == f(x)
right_identity_holds = Ok(8).bind(unit) == Ok(8)  # => m.bind(unit) == m
associativity_holds = Ok(8).bind(half).bind(add_ten) == Ok(
    8
).bind(  # => m.bind(f).bind(g)
    lambda x: half(x).bind(add_ten)  # => == m.bind(lambda x: f(x).bind(g))
)  # => closes the associativity check's multi-line expression

# => these three laws are what makes 'monad' a precise term, not just a vague design pattern
print(left_identity_holds)  # => Output: True
print(right_identity_holds)  # => Output: True
print(associativity_holds)  # => Output: True

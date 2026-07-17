"""Example 56: bind/flat_map Chaining Result Steps."""

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
)  # => Generic/TypeVar/Callable type the bind chain below

T = TypeVar("T")  # => the type of the value an Ok wraps
U = TypeVar("U")  # => the type bind's step function returns
E = TypeVar("E")  # => the type of the error an Err wraps
F = TypeVar(
    "F"
)  # => the error type threaded through bind's step function, not hardcoded to object


@dataclass(frozen=True)  # => marks Ok immutable, matching the FP style
class Ok(Generic[T]):  # => the success variant's body
    value: T  # => the single field this variant carries

    def bind(
        self, fn: Callable[[T], "Result[U, F]"]
    ) -> "Result[U, F]":  # => F comes from fn's OWN error type
        # => bind/and_then/flat_map -- three names for the SAME monadic chaining operation
        return fn(
            self.value
        )  # => unwraps, runs fn (which itself returns a Result), no double-wrap


@dataclass(frozen=True)  # => marks Err immutable too
class Err(Generic[E]):  # => the failure variant's body
    error: E  # => the single field this variant carries

    def bind(
        self, fn: Callable[[T], U]
    ) -> "Err[E]":  # => NO-OP, generic so a typed fn still passes the check
        return self  # => fn never runs once the chain has already failed


Result = Ok[T] | Err[E]  # => the ADT itself: a Result is EITHER variant


def half(n: int) -> "Result[float, str]":  # => a bind STEP: fails if n is odd
    if n % 2 != 0:  # => the ONLY failure condition this step checks
        return Err(f"{n} is odd")  # => switches to the failure track
    return Ok(n / 2)  # => the success track: n halved


def to_positive(
    x: float,
) -> "Result[float, str]":  # => a second bind STEP: fails if not positive
    return (
        Ok(x) if x > 0 else Err(f"{x} is not positive")
    )  # => the second bind step: may succeed or fail


chained_success = Ok(8).bind(half).bind(to_positive)  # => 8 -> 4.0 -> still positive
chained_failure = (
    Ok(7).bind(half).bind(to_positive)
)  # => 7 is odd -- fails at the FIRST bind

print(chained_success)  # => Output: Ok(value=4.0)
print(chained_failure)  # => Output: Err(error='7 is odd')

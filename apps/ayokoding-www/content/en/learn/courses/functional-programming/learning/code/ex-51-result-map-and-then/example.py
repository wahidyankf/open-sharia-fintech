"""Example 51: map and and_then on a Result."""

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
)  # => Generic/TypeVar/Callable type the map and and_then methods

T = TypeVar("T")  # => the type of the value an Ok wraps
U = TypeVar("U")  # => the type map/and_then transform T into
E = TypeVar("E")  # => the type of the error an Err wraps
F = TypeVar(
    "F"
)  # => the error type threaded through and_then's step function, not hardcoded to object


@dataclass(frozen=True)  # => marks Ok immutable, matching the FP style
class Ok(Generic[T]):  # => the success variant's body
    value: T  # => the single field this variant carries

    def map(
        self, fn: Callable[[T], U]
    ) -> "Result[U, object]":  # => transforms the SUCCESS value only
        return Ok(fn(self.value))  # => transforms the value, stays wrapped as Ok

    def and_then(  # => chains into ANOTHER Result-returning step, without double-wrapping
        self,
        fn: Callable[
            [T], "Result[U, F]"
        ],  # => F is inferred from fn's own error type, not widened to object
    ) -> "Result[U, F]":  # => the chained Result keeps fn's REAL error type
        return fn(
            self.value
        )  # => runs fn on the unwrapped value; fn itself returns a Result


@dataclass(frozen=True)  # => marks Err immutable too
class Err(Generic[E]):  # => the failure variant's body
    error: E  # => the single field this variant carries

    def map(
        self, fn: Callable[[T], U]
    ) -> "Err[E]":  # => NO-OP: generic so a typed fn still passes the check
        return self  # => the error passes through UNCHANGED -- fn never runs

    def and_then(
        self, fn: Callable[[T], U]
    ) -> "Err[E]":  # => and_then is ALSO a no-op on Err, generic likewise
        return self  # => short-circuits: fn never runs once the pipeline has already failed


Result = Ok[T] | Err[E]  # => the ADT itself: a Result is EITHER variant


def parse_positive(
    text: str,
) -> "Result[int, str]":  # => an and_then STEP: str -> Result[int, str]
    value = int(text)  # => may raise, but this example only feeds it valid ints
    return (
        Ok(value) if value > 0 else Err(f"{value} is not positive")
    )  # => the and_then step itself: may succeed or fail


times_ten: Callable[[int], int] = lambda n: (
    n * 10
)  # => explicit annotation pins map's generic parameter to int

ok_chain = Ok("5").and_then(parse_positive).map(times_ten)  # => success end to end
err_chain = Ok("-5").and_then(parse_positive).map(times_ten)  # => fails at and_then

# => map transforms success; and_then chains into ANOTHER fallible step
print(ok_chain)  # => Output: Ok(value=50)
print(err_chain)  # => Output: Err(error='-5 is not positive')

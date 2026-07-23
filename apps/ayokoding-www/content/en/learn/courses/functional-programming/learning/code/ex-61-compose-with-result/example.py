"""Example 61: Composing Result-Returning Functions (Kleisli Composition)."""

from __future__ import (
    annotations,
)  # => enables the quoted 'Result[U, str]' forward references below

from dataclasses import (
    dataclass,
)  # => @dataclass(frozen=True) builds both Result variants
from typing import (
    Callable,
    Generic,
    TypeVar,
)  # => Generic/TypeVar/Callable type kleisli_compose below

T = TypeVar("T")  # => the type kleisli_compose's INPUT function consumes
U = TypeVar("U")  # => the type kleisli_compose's OUTPUT function produces
E = TypeVar("E")  # => the type of the error an Err wraps


@dataclass(frozen=True)  # => marks Ok immutable, matching the FP style
class Ok(Generic[T]):  # => the success variant's body
    value: T  # => the single field this variant carries


@dataclass(frozen=True)  # => marks Err immutable too
class Err(Generic[E]):  # => the failure variant's body
    error: E  # => the single field this variant carries


Result = Ok[T] | Err[E]  # => the ADT itself: a Result is EITHER variant


def kleisli_compose(  # => composes TWO Result-returning functions into ONE, like compose but Result-aware
    f: Callable[[T], "Result[U, str]"],
    g: Callable[[U], "Result[U, str]"],  # => the two steps kleisli_compose chains
) -> Callable[[T], "Result[U, str]"]:  # => closes the multi-line signature above
    def composed(
        x: T,
    ) -> "Result[U, str]":  # => the returned, composed pipeline function
        first = f(x)  # => runs the FIRST step
        if isinstance(
            first, Err
        ):  # => short-circuits: g never runs if f already failed
            return first  # => propagates f's failure untouched
        return g(first.value)  # => chains g onto f's unwrapped success value

    return composed  # => kleisli_compose itself returns the composed pipeline function


def parse_int(text: str) -> "Result[int, str]":  # => step 1: str -> Result[int, str]
    try:  # => attempts the conversion
        return Ok(int(text))  # => success: wraps the parsed int
    except ValueError:  # => text was not a valid integer
        return Err(
            f"'{text}' is not an integer"
        )  # => the error travels as an ordinary VALUE


def reciprocal(n: int) -> "Result[int, str]":  # => step 2: int -> Result[int, str]
    if n == 0:  # => the ONLY failure condition this step checks
        return Err(
            "cannot take the reciprocal of zero"
        )  # => switches to the failure track
    return Ok(
        1 // n if n == 1 else 0
    )  # => simplified integer reciprocal, just for this example


pipeline = kleisli_compose(
    parse_int, reciprocal
)  # => ONE composed function: str -> Result[int, str]

# => Kleisli composition is compose specialized to Result-returning functions
print(pipeline("1"))  # => Output: Ok(value=1)
print(pipeline("0"))  # => Output: Err(error='cannot take the reciprocal of zero')
print(pipeline("x"))  # => Output: Err(error="'x' is not an integer")

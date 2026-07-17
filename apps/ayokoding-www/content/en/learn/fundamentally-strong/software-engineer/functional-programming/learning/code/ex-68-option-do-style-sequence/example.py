"""Example 68: Sequencing Option Computations, Do-Style."""

from __future__ import (
    annotations,
)  # => enables the quoted 'Option[U]' forward reference below

from dataclasses import (
    dataclass,
)  # => @dataclass(frozen=True) builds both Option variants
from typing import (
    Callable,
    Generic,
    TypeVar,
)  # => Generic/TypeVar/Callable type and_then below

T = TypeVar("T")  # => the type of the value a Some wraps
U = TypeVar("U")  # => the type and_then's step function returns


@dataclass(frozen=True)  # => marks Some immutable, matching the FP style
class Some(Generic[T]):  # => the class body begins here
    value: T  # => the single field this variant carries

    def and_then(
        self, fn: Callable[[T], "Option[U]"]
    ) -> "Option[U]":  # => the sequencing operation
        return fn(
            self.value
        )  # => runs fn on the unwrapped value; fn itself returns an Option


@dataclass(frozen=True)  # => marks Nothing immutable too
class Nothing:  # => the class body begins here
    def and_then(
        self, fn: Callable[[T], U]
    ) -> "Nothing":  # => short-circuits, generic so union calls stay typed
        return self  # => Nothing stays Nothing, regardless of fn


Option = Some[T] | Nothing  # => the ADT itself: an Option is EITHER variant


def safe_div(
    a: float, b: float
) -> "Option[float]":  # => a step that may be absent (division by zero)
    return (
        Nothing() if b == 0 else Some(a / b)
    )  # => success wraps, failure returns Nothing


def safe_sqrt(
    x: float,
) -> "Option[float]":  # => a step that may be absent (negative input)
    return (
        Nothing() if x < 0 else Some(x**0.5)
    )  # => success wraps, failure returns Nothing


def sqrt_step(
    ratio: float,
) -> (
    "Option[float]"
):  # => named + typed and_then step -- a bare lambda can't carry annotations
    return safe_sqrt(
        ratio
    )  # => same behavior as the inline version, now with a concrete float param


def scale_step(
    root: float,
) -> "Option[float]":  # => named + typed and_then step, same reasoning
    return Some(root * 100)  # => wraps the scaled result back into Some


def compute(
    a: float, b: float
) -> "Option[float]":  # => "do-style": each step reads like a statement
    return (  # => opens the do-style chain of and_then calls
        safe_div(a, b)  # => step 1
        .and_then(sqrt_step)  # => step 2, only runs if step 1 succeeded
        .and_then(scale_step)  # => step 3, only runs if step 2 succeeded
    )  # => closes the do-style chain of and_then calls


# => chained and_then calls read like a sequence of statements, not nested callbacks
print(compute(100, 4))  # => Output: Some(value=500.0)
print(compute(100, 0))  # => Output: Nothing() -- short-circuits at the FIRST step
print(compute(-100, 4))  # => Output: Nothing() -- short-circuits at the SECOND step

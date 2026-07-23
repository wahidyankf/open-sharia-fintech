"""Example 79: The Same Pipeline in Option vs. Result."""

from __future__ import (
    annotations,
)  # => enables the quoted forward references used below

from dataclasses import (
    dataclass,
)  # => @dataclass(frozen=True) builds all four variants below
from typing import (
    Callable,
    Generic,
    TypeVar,
)  # => Generic/TypeVar/Callable type both and_then methods

T = TypeVar("T")  # => the type of the value a Some or Ok wraps
U = TypeVar("U")  # => the type each and_then's step function returns


@dataclass(frozen=True)  # => marks Some immutable, matching the FP style
class Some(Generic[T]):  # => the class body begins here
    value: T  # => the single field this variant carries

    def and_then(
        self, fn: Callable[[T], "Option[U]"]
    ) -> "Option[U]":  # => Option's chaining operation
        return fn(self.value)  # => runs fn on the unwrapped value


@dataclass(frozen=True)  # => marks Nothing immutable too
class Nothing:  # => the class body begins here
    def and_then(
        self, fn: Callable[[T], U]
    ) -> "Nothing":  # => short-circuits, generic so union calls stay typed
        return self  # => Nothing carries NO explanation for why


Option = Some[T] | Nothing  # => the Option ADT: EITHER variant


@dataclass(frozen=True)  # => marks Ok immutable, matching the FP style
class Ok(Generic[T]):  # => the class body begins here
    value: T  # => the single field this variant carries

    def and_then(
        self, fn: Callable[[T], "Res[U]"]
    ) -> "Res[U]":  # => Result's chaining operation
        return fn(self.value)  # => runs fn on the unwrapped value


@dataclass(frozen=True)  # => marks Err immutable too
class Err:  # => the class body begins here
    error: str  # => Result CARRIES a reason -- Option's Nothing cannot

    def and_then(
        self, fn: Callable[[T], U]
    ) -> "Err":  # => short-circuits, generic so union calls stay typed
        return self  # => the REASON rides through untouched


Res = Ok[T] | Err  # => the Result ADT: EITHER variant


def parse_option(
    text: str,
) -> "Option[int]":  # => same parsing logic, Option's error model: just absence
    return (
        Some(int(text)) if text.isdigit() else Nothing()
    )  # => success wraps, failure loses all context


def parse_result(
    text: str,
) -> "Res[int]":  # => same parsing logic, Result's error model: WHY it failed
    return (
        Ok(int(text)) if text.isdigit() else Err(f"'{text}' is not a digit string")
    )  # => failure keeps context


def double_option(
    n: int,
) -> (
    "Option[int]"
):  # => named + typed -- a bare lambda loses its param type on the union call
    return Some(
        n * 2
    )  # => same "double" step as double_result, wrapped in Option's variant


def double_result(
    n: int,
) -> "Res[int]":  # => named + typed, same reasoning as double_option
    return Ok(
        n * 2
    )  # => same "double" step as double_option, wrapped in Result's variant


option_pipeline = parse_option("42").and_then(double_option)  # => Option pipeline
result_pipeline = parse_result("42").and_then(
    double_result
)  # => Result pipeline, same shape

option_failure = parse_option("bad")  # => Nothing -- no explanation attached
result_failure = parse_result("bad")  # => Err carrying a human-readable reason

# => the SAME chain, two error models -- pick based on whether the reason matters
print(option_pipeline)  # => Output: Some(value=84)
print(result_pipeline)  # => Output: Ok(value=84)
print(option_failure)  # => Output: Nothing() -- WHY it failed is not represented at all
print(
    result_failure
)  # => Output: Err(error="'bad' is not a digit string") -- the reason IS represented

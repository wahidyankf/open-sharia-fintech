"""Example 50: A Hand-Rolled Ok/Err Result Type."""

from __future__ import (
    annotations,
)  # => enables the quoted 'Result[float, str]' forward reference below

from dataclasses import (
    dataclass,
)  # => @dataclass(frozen=True) builds both Result variants
from typing import (
    Generic,
    TypeVar,
)  # => Generic/TypeVar make Ok[T] and Err[E] proper generic containers

T = TypeVar("T")  # => the type of the value an Ok wraps
E = TypeVar("E")  # => the type of the error an Err wraps


@dataclass(frozen=True)  # => marks Ok immutable, matching the FP style
class Ok(Generic[T]):  # => the "success" variant, carrying the computed value
    value: T  # => the single field this variant carries


@dataclass(frozen=True)  # => marks Err immutable too
class Err(
    Generic[E]
):  # => the "failure" variant, carrying the ERROR AS A VALUE, not an exception
    error: E  # => the single field this variant carries


Result = Ok[T] | Err[E]  # => PEP 604 union: a Result is either Ok[T] or Err[E]


def divide(
    a: int, b: int
) -> "Result[float, str]":  # => the failure mode is IN the return type
    if b == 0:  # => a caller reading this signature already knows failure is possible
        return Err("division by zero")  # => the error travels as an ordinary VALUE
    return Ok(a / b)  # => success wraps the computed value


success = divide(10, 2)  # => Ok(5.0)
failure = divide(10, 0)  # => Err('division by zero') -- NO exception was raised

# => Result makes failure part of the TYPE, not a hidden exception path
print(success)  # => Output: Ok(value=5.0)
print(failure)  # => Output: Err(error='division by zero')
print(
    isinstance(failure, Err)
)  # => Output: True -- the caller can inspect this without a try/except

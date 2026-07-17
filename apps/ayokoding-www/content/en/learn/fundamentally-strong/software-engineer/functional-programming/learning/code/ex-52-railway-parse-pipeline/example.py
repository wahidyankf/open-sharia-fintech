"""Example 52: A Validation Pipeline Threading Result."""

from __future__ import (
    annotations,
)  # => enables the quoted 'Result[int, str]' forward references below

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
class Ok(Generic[T]):  # => the success variant's body
    value: T  # => the single field this variant carries


@dataclass(frozen=True)  # => marks Err immutable too
class Err(Generic[E]):  # => the failure variant's body
    error: E  # => the single field this variant carries


Result = Ok[T] | Err[E]  # => the ADT itself: a Result is EITHER variant


def validate_age(
    age: int,
) -> "Result[int, str]":  # => railway step 1: switches to the failure track on error
    if age < 0:  # => the ONLY failure condition this step checks
        return Err("age cannot be negative")  # => switches to the failure track
    return Ok(age)  # => the success track, value unchanged


def validate_name(name: str) -> "Result[str, str]":  # => railway step 2
    if not name:  # => the ONLY failure condition this step checks
        return Err("name cannot be empty")  # => switches to the failure track
    return Ok(name)  # => the success track, value unchanged


def validate_form(
    name: str, age: int
) -> "Result[str, str]":  # => threads BOTH steps in sequence
    name_result = validate_name(name)  # => the FIRST switch point
    if isinstance(
        name_result, Err
    ):  # => already on the failure track -- age is never checked
        return name_result  # => the original error rides through untouched
    age_result = validate_age(
        age
    )  # => the SECOND switch point, only reached if step 1 succeeded
    if isinstance(age_result, Err):  # => the SECOND switch point
        return age_result  # => propagates the second step's failure
    return Ok(f"{name_result.value}, age {age_result.value}")  # => both checks passed


valid = validate_form("Ana", 30)  # => both checks succeed
bad_name = validate_form(
    "", 30
)  # => fails at the FIRST check -- age is never even validated
bad_age = validate_form("Ana", -1)  # => passes name, fails at the SECOND check

# => this is the railway-oriented programming pattern: one track, two rails
print(valid)  # => Output: Ok(value='Ana, age 30')
print(bad_name)  # => Output: Err(error='name cannot be empty')
print(bad_age)  # => Output: Err(error='age cannot be negative')

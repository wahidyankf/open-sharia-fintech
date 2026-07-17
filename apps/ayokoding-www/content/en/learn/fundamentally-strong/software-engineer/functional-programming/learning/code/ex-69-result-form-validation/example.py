"""Example 69: Validating a Form, Short-Circuiting on the First Failing Rule."""

from __future__ import (
    annotations,
)  # => enables the quoted 'Result[str, str]' forward references below

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
class Ok(Generic[T]):  # => the class body begins here
    value: T  # => the single field this variant carries


@dataclass(frozen=True)  # => marks Err immutable too
class Err(Generic[E]):  # => the class body begins here
    error: E  # => the single field this variant carries


Result = Ok[T] | Err[E]  # => the ADT itself: a Result is EITHER variant


def check_username(username: str) -> "Result[str, str]":  # => rule 1
    return (
        Ok(username) if len(username) >= 3 else Err("username too short")
    )  # => the ONLY check this rule makes


def check_password(password: str) -> "Result[str, str]":  # => rule 2
    return (
        Ok(password) if len(password) >= 8 else Err("password too short")
    )  # => the ONLY check this rule makes


def check_age(age: int) -> "Result[int, str]":  # => rule 3
    return (
        Ok(age) if age >= 13 else Err("must be at least 13")
    )  # => the ONLY check this rule makes


def validate_signup(
    username: str, password: str, age: int
) -> "Result[str, str]":  # => threads all 3 rules
    username_result = check_username(username)  # => rule 1's switch point
    if isinstance(username_result, Err):  # => STOP: rules 2 and 3 never run
        return username_result  # => reports THIS rule as the failing one
    password_result = check_password(password)  # => rule 2's switch point
    if isinstance(password_result, Err):  # => STOP: rule 3 never runs
        return password_result  # => reports THIS rule as the failing one
    age_result = check_age(age)  # => rule 3's switch point
    if isinstance(age_result, Err):  # => the last possible failure point
        return age_result  # => reports THIS rule as the failing one
    return Ok(f"welcome, {username_result.value}")  # => all three rules passed


# => real forms usually have more than two fields -- this scales the railway pattern to three
print(validate_signup("ana", "longenough", 20))  # => Output: Ok(value='welcome, ana')
print(
    validate_signup("an", "longenough", 20)
)  # => Output: Err(error='username too short')
print(validate_signup("ana", "short", 20))  # => Output: Err(error='password too short')
print(
    validate_signup("ana", "longenough", 10)
)  # => Output: Err(error='must be at least 13')

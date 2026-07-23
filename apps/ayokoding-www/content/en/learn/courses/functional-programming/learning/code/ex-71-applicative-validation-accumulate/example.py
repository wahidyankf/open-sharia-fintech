"""Example 71: An Applicative Validation That Accumulates All Errors."""

from __future__ import (
    annotations,
)  # => enables the quoted 'Validated[T]' forward references below

from dataclasses import (
    dataclass,
)  # => @dataclass(frozen=True) builds both Validated variants
from typing import (
    Generic,
    TypeVar,
)  # => Generic/TypeVar make Valid[T] a proper generic container

T = TypeVar("T")  # => the type of the value a Valid wraps


@dataclass(frozen=True)  # => success, carrying the validated value
class Valid(Generic[T]):  # => the class body begins here
    value: T  # => the single field this variant carries


@dataclass(frozen=True)  # => failure, carrying EVERY error found, not just the first
class Invalid:  # => the class body begins here
    errors: tuple[
        str, ...
    ]  # => one entry per failing rule, accumulated across all checks


Validated = (
    Valid[T] | Invalid
)  # => this topic's SECOND Result-shaped type -- accumulates instead of short-circuits


def validate_username(
    username: str,
) -> "Validated[str]":  # => rule 1, independent of the others
    return (
        Valid(username) if len(username) >= 3 else Invalid(("username too short",))
    )  # => the ONLY check this rule makes


def validate_password(
    password: str,
) -> "Validated[str]":  # => rule 2, independent of the others
    return (
        Valid(password) if len(password) >= 8 else Invalid(("password too short",))
    )  # => the ONLY check this rule makes


def validate_age(age: int) -> "Validated[int]":  # => rule 3, independent of the others
    return (
        Valid(age) if age >= 13 else Invalid(("must be at least 13",))
    )  # => the ONLY check this rule makes


def combine3(  # => the applicative combinator: runs ALL THREE checks, merges ALL failures
    a: "Validated[str]",
    b: "Validated[str]",
    c: "Validated[int]",  # => the three independent checks to combine
) -> "Validated[str]":  # => closes the multi-line signature above
    errors: list[str] = []  # => collects failures from EVERY input, not just the first
    for result in (
        a,
        b,
        c,
    ):  # => visits all three, regardless of whether earlier ones already failed
        if isinstance(result, Invalid):  # => this particular check failed
            errors.extend(
                result.errors
            )  # => appends THIS check's errors onto the running list
    if errors:  # => at least one check failed
        return Invalid(
            tuple(errors)
        )  # => reports EVERY failing rule, not just the first
    return Valid(f"welcome, {a.value}")  # type: ignore[union-attr]  # => all three checks passed


all_valid = combine3(
    validate_username("ana"), validate_password("longenough"), validate_age(20)
)  # => every check passes
all_invalid = combine3(
    validate_username("an"), validate_password("short"), validate_age(10)
)  # => every check fails

# => this is railway-oriented programming's opposite: gather everything, stop for nothing
print(all_valid)  # => Output: Valid(value='welcome, ana')
print(
    all_invalid
)  # => Output: Invalid(errors=('username too short', 'password too short', 'must be at least 13'))

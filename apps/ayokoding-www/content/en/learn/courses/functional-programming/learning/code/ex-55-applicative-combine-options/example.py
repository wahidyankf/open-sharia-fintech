"""Example 55: map2 Combines Two Options."""

from __future__ import (
    annotations,
)  # => enables the quoted 'Option[V]' forward reference below

from dataclasses import (
    dataclass,
)  # => @dataclass(frozen=True) builds both Option variants
from typing import (
    Callable,
    Generic,
    TypeVar,
)  # => Generic/TypeVar/Callable type the applicative map2 below

T = TypeVar("T")  # => the type of the first wrapped value
U = TypeVar("U")  # => the type of the second wrapped value
V = TypeVar("V")  # => the type fn returns after combining both


@dataclass(frozen=True)  # => marks Some immutable, matching the FP style
class Some(Generic[T]):  # => the present variant's body
    value: T  # => the single field this variant carries


@dataclass(frozen=True)  # => marks Nothing immutable too
class Nothing:  # => the absent variant's body
    pass  # => carries no data at all


Option = Some[T] | Nothing  # => the ADT itself: an Option is EITHER variant


def map2(  # => the applicative pattern: combine TWO wrapped values with a 2-arg function
    fn: Callable[[T, U], V],
    opt_a: "Option[T]",
    opt_b: "Option[U]",  # => the 2-arg combiner plus the two Options it combines
) -> "Option[V]":  # => closes the multi-line signature above
    if isinstance(opt_a, Nothing) or isinstance(
        opt_b, Nothing
    ):  # => EITHER absent short-circuits
        return Nothing()  # => no partial combination -- both-or-nothing
    return Some(
        fn(opt_a.value, opt_b.value)
    )  # => both present: unwrap both, apply fn, rewrap


def add(
    a: int, b: int
) -> int:  # => the 2-argument function map2 combines two Options with
    return a + b  # => the actual addition add performs


both_present = map2(add, Some(2), Some(3))  # => both wrapped values ARE present
one_missing = map2(add, Some(2), Nothing())  # => the second value is ABSENT

# => applicative map2 generalizes map to functions of MORE than one argument
print(both_present)  # => Output: Some(value=5)
print(one_missing)  # => Output: Nothing()

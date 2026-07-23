"""Example 48: A Hand-Rolled Some/Nothing With map."""

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
)  # => Generic/TypeVar make Some[T] a proper generic container

T = TypeVar("T")  # => the type of the value a Some wraps
U = TypeVar("U")  # => the type map's function returns


@dataclass(frozen=True)  # => marks Some immutable, matching the FP style
class Some(Generic[T]):  # => the "present" variant, carrying exactly one value
    value: T  # => the single field this variant carries

    def map(
        self, fn: Callable[[T], U]
    ) -> "Option[U]":  # => applies fn INSIDE the wrapper
        return Some(fn(self.value))  # => stays wrapped -- Some in, Some out


@dataclass(frozen=True)  # => marks Nothing immutable too
class Nothing:  # => the "absent" variant, carrying nothing
    def map(
        self, fn: Callable[[T], U]
    ) -> "Nothing":  # => NO-OP: still generic so it type-checks like Some.map
        return self  # => there is nothing to apply fn to -- Nothing stays Nothing


Option = (
    Some[T] | Nothing
)  # => PEP 604 union: an Option[T] is either Some[T] or Nothing


present: Option[int] = Some(5)  # => an Option holding a real value
absent: Option[int] = Nothing()  # => an Option holding nothing at all

increment: Callable[[int], int] = lambda x: (
    x + 1
)  # => explicit annotation pins T/U to int at both call sites
mapped_present = present.map(increment)  # => Some(5).map(+1) -- the function DOES run
mapped_absent = absent.map(
    increment
)  # => Nothing.map(+1) -- the function is SKIPPED entirely

# => Option replaces None with a type the reader (and a type checker) can reason about
print(mapped_present)  # => Output: Some(value=6)
print(mapped_absent)  # => Output: Nothing()
print(
    mapped_absent == Nothing()
)  # => Output: True -- map never turns Nothing into Some

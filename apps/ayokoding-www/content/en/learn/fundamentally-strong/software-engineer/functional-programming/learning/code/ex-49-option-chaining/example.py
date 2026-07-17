"""Example 49: Chaining Option-Returning Lookups."""

from __future__ import (
    annotations,
)  # => enables the quoted 'Option[T]' forward reference below

from dataclasses import (
    dataclass,
)  # => @dataclass(frozen=True) builds both Option variants
from typing import (
    Generic,
    TypeVar,
)  # => Generic/TypeVar make Some[T] a proper generic container

T = TypeVar("T")  # => the type of the value a Some wraps


@dataclass(frozen=True)  # => marks Some immutable, matching the FP style
class Some(Generic[T]):  # => the "present" variant, carrying exactly one value
    value: T  # => the single field this variant carries


@dataclass(frozen=True)  # => marks Nothing immutable too
class Nothing:  # => the "absent" variant
    pass  # => carries no data at all


Option = Some[T] | Nothing  # => the ADT itself: an Option is EITHER variant


def find(
    table: dict[str, T], key: str
) -> "Option[T]":  # => an Option-returning lookup, no None
    return (
        Some(table[key]) if key in table else Nothing()
    )  # => success wraps, miss returns Nothing


def find_user_then_city(  # => opens the multi-line signature of the chained lookup
    users: dict[str, str],
    cities: dict[str, str],
    username: str,  # => the two lookup tables plus the key to chase
) -> "Option[str]":  # => closes the multi-line signature above
    user_result = find(users, username)  # => first Option-returning lookup
    if isinstance(
        user_result, Nothing
    ):  # => SHORT-CIRCUITS immediately on the first miss
        return Nothing()  # => never even attempts the second lookup
    return find(
        cities, user_result.value
    )  # => chains into a SECOND Option-returning lookup


users = {"ana": "jakarta"}  # => maps username -> city key
cities = {"jakarta": "Jakarta, Indonesia"}  # => maps city key -> display name

hit = find_user_then_city(users, cities, "ana")  # => both lookups succeed
miss = find_user_then_city(users, cities, "budi")  # => the FIRST lookup already misses

# => chaining Option lookups avoids nested None-checks entirely
print(hit)  # => Output: Some(value='Jakarta, Indonesia')
print(miss)  # => Output: Nothing()

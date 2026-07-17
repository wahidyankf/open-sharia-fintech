"""Example 54: One fmap Working on list and Option."""

from __future__ import (
    annotations,
)  # => enables the quoted 'Option[T]' forward references below

from dataclasses import (
    dataclass,
)  # => @dataclass(frozen=True) builds both Option variants
from typing import (
    Callable,
    Generic,
    TypeVar,
)  # => Generic/TypeVar/Callable type the shared fmap below

T = TypeVar("T")  # => the type of the value a container wraps
U = TypeVar("U")  # => the type fn transforms T into


@dataclass(frozen=True)  # => marks Some immutable, matching the FP style
class Some(Generic[T]):  # => the present variant's body
    value: T  # => the single field this variant carries


@dataclass(frozen=True)  # => marks Nothing immutable too
class Nothing:  # => the absent variant's body
    pass  # => carries no data at all


Option = Some[T] | Nothing  # => the ADT itself: an Option is EITHER variant


def fmap(
    fn: Callable[[T], U], container: "list[T] | Some[T] | Nothing"
) -> object:  # => ONE signature, THREE possible container shapes
    # => ONE function, dispatching on the container's actual shape -- the functor pattern made concrete
    if isinstance(container, list):  # => a list is mappable via a comprehension
        return [fn(item) for item in container]  # => applies fn to every element
    if isinstance(container, Some):  # => an Option is mappable via its own map rule
        return Some(fn(container.value))  # => applies fn to the single wrapped value
    return Nothing()  # => Nothing maps to Nothing, regardless of fn


double: Callable[[int], int] = lambda n: (
    n * 2
)  # => explicit annotation lets fmap solve T=int from fn, not the lambda body

mapped_list = fmap(double, [1, 2, 3])  # => the list case
mapped_some = fmap(double, Some(5))  # => the Option case, present
mapped_nothing = fmap(double, Nothing())  # => the Option case, absent

print(mapped_list)  # => Output: [2, 4, 6]
print(mapped_some)  # => Output: Some(value=10)
print(mapped_nothing)  # => Output: Nothing()

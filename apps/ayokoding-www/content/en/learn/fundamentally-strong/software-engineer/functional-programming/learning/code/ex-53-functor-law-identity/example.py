"""Example 53: The Functor Identity Law by Example."""

from __future__ import (
    annotations,
)  # => enables the quoted 'Box[U]' forward reference below

from dataclasses import dataclass  # => @dataclass(frozen=True) builds the immutable Box
from typing import (
    Callable,
    Generic,
    TypeVar,
)  # => Generic/TypeVar/Callable type the minimal functor below

T = TypeVar("T")  # => the type of the value a Box wraps
U = TypeVar("U")  # => the type map's function returns


def identity(x: T) -> T:  # => the identity function: returns its argument UNCHANGED
    return x  # => identity's entire body: returns its argument, unchanged


@dataclass(frozen=True)  # => marks Box immutable, matching the FP style
class Box(Generic[T]):  # => a minimal functor: any container with a lawful map
    value: T  # => the single field this container carries

    def map(
        self, fn: Callable[[T], U]
    ) -> "Box[U]":  # => applies fn inside, stays wrapped
        return Box(fn(self.value))  # => applies fn inside, re-wraps as Box


original = Box(42)  # => the container BEFORE the identity law is applied
mapped_with_identity = original.map(identity)  # => container.map(identity)

# => the functor identity law is a correctness check any lawful map must pass
print(
    mapped_with_identity == original
)  # => Output: True -- the FUNCTOR IDENTITY LAW, verified
print(
    mapped_with_identity is original
)  # => Output: False -- EQUAL, but a distinct object (still immutable)

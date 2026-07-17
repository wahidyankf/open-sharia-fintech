"""Example 70: Property-Checking the Functor Identity and Composition Laws."""

import random  # => stdlib source of pseudo-random Box values -- no third-party library needed
from dataclasses import dataclass  # => @dataclass(frozen=True) builds the immutable Box
from typing import (
    Callable,
    Generic,
    TypeVar,
)  # => Generic/TypeVar/Callable type the functor below

T = TypeVar("T")  # => the type of the value a Box wraps
U = TypeVar("U")  # => the type map's function returns


@dataclass(frozen=True)  # => the functor under test
class Box(Generic[T]):  # => the class body begins here
    value: T  # => the single field this container carries

    def map(
        self, fn: Callable[[T], U]
    ) -> "Box[U]":  # => applies fn inside, stays wrapped
        return Box(fn(self.value))  # => applies fn inside, re-wraps as Box


def identity(x: int) -> int:  # => the identity function, used by the identity law
    return x  # => returns its argument unchanged


def add_one(x: int) -> int:  # => one of the two functions used by the composition law
    return x + 1  # => the actual +1


def double(x: int) -> int:  # => the second function used by the composition law
    return x * 2  # => the actual *2


def check_identity_law(box: "Box[int]") -> bool:  # => box.map(identity) == box
    return box.map(identity) == box  # => the identity law's own definition


def check_composition_law(
    box: "Box[int]",
) -> bool:  # => box.map(f).map(g) == box.map(compose(g, f))
    mapped_twice = box.map(add_one).map(
        double
    )  # => two SEPARATE map calls, one after another
    mapped_once = box.map(
        lambda x: double(add_one(x))
    )  # => ONE map call with the composed function
    return mapped_twice == mapped_once  # => the composition law's own definition


random.seed(42)  # => fixed seed -- this property check is fully reproducible
generated_boxes = [
    Box(random.randint(-1000, 1000)) for _ in range(300)
]  # => 300 random Box values

identity_law_holds = all(
    check_identity_law(b) for b in generated_boxes
)  # => checks ALL 300, not one
composition_law_holds = all(
    check_composition_law(b) for b in generated_boxes
)  # => checks ALL 300, not one

# => checking BOTH functor laws together is what makes a map implementation trustworthy
print(identity_law_holds)  # => Output: True
print(composition_law_holds)  # => Output: True

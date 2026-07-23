"""Example 75: Measuring Persistent-Update Cost vs. In-Place Mutation."""

import time  # => times both code paths for a rough, qualitative comparison
from dataclasses import (
    dataclass,
    replace,
)  # => replace builds a NEW ImmutablePoint from an OLD one


@dataclass(
    frozen=True
)  # => the IMMUTABLE version: every "update" allocates a new object
class ImmutablePoint:  # => the class body begins here
    x: int  # => the coordinate this example bumps repeatedly
    y: int  # => unused by this example, kept for a realistic shape


class MutablePoint:  # => the MUTABLE version: "update" writes in place, no allocation
    def __init__(self, x: int, y: int) -> None:  # => an ordinary, non-frozen class
        self.x = x  # => a plain, mutable attribute
        self.y = y  # => a plain, mutable attribute


def bump_immutable(
    p: ImmutablePoint, n: int
) -> ImmutablePoint:  # => allocates a NEW object each call
    for _ in range(n):  # => repeats the "update" n times
        p = replace(
            p, x=p.x + 1
        )  # => n allocations total -- one frozen dataclass per step
    return p  # => the final, newest ImmutablePoint


def bump_mutable(
    p: MutablePoint, n: int
) -> MutablePoint:  # => mutates the SAME object each call
    for _ in range(n):  # => repeats the "update" n times
        p.x += 1  # => zero extra allocations -- writes directly into existing memory
    return p  # => the SAME object, just with x changed n times


iterations = 200_000  # => enough repetitions to make the cost difference measurable

start = time.perf_counter()  # => marks the start of the immutable-path timing
result_immutable = bump_immutable(
    ImmutablePoint(0, 0), iterations
)  # => n allocations happen here
immutable_seconds = time.perf_counter() - start  # => elapsed time for n allocations

start = time.perf_counter()  # => marks the start of the mutable-path timing
result_mutable = bump_mutable(
    MutablePoint(0, 0), iterations
)  # => n in-place writes happen here
mutable_seconds = time.perf_counter() - start  # => elapsed time for n in-place writes

# => this is the honest cost side of the immutability trade-off this topic advocates
print(
    result_immutable.x == result_mutable.x == iterations
)  # => Output: True -- BOTH reach the correct answer
print(
    immutable_seconds > 0 and mutable_seconds > 0
)  # => Output: True -- both measured a nonzero duration

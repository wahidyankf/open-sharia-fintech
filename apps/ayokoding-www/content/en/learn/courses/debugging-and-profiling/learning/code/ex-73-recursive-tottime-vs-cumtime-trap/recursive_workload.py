"""Example 73: a recursive function whose wrapper's cumtime looks alarming, but
whose OWN tottime (self time) is tiny -- the real hot spot is a leaf function
called deep inside the recursion, not the recursive wrapper itself.
"""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the recursion itself


def expensive_leaf(
    n: int,
) -> int:  # => co-16/co-13: the REAL hot spot -- called ONCE per recursion level, real Python work
    # co-16: the REAL hot spot -- pure Python work, called once per recursion level.
    total = 0  # => co-16: accumulator -- its final value is irrelevant, only the WORK time matters here
    for i in range(
        n
    ):  # => co-16: n iterations of pure interpreter work -- genuinely expensive, unlike the wrapper below
        total += (
            i * i
        )  # => co-16: cheap per-iteration math -- keeps this CPU-bound, not memory-bound
    return total  # => co-16: discarded by every caller -- only cProfile's OWN measurement of this call matters here


def recursive_wrapper(
    depth: int, work_size: int
) -> int:  # => co-16: the TRAP -- huge cumtime, tiny tottime
    # co-16: this function's CUMULATIVE time is nearly the whole program (it
    # contains all the recursion), but its OWN tottime is just one comparison,
    # one subtraction, and one addition per call -- almost nothing.
    if (
        depth == 0
    ):  # => co-16: the base case -- depth counts DOWN to zero across the recursive calls below
        return 0  # => co-16: the recursion's floor -- contributes nothing to expensive_leaf's own total
    return expensive_leaf(work_size) + recursive_wrapper(
        depth - 1, work_size
    )  # => co-16: ONE leaf call, ONE recursive call

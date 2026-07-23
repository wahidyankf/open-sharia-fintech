"""Example 79: Immutable vs Mutable Performance."""

import time  # => wall-clock timing is the whole point of this comparison

N = 20000  # => number of updates -- large enough to produce a measurable, stable timing difference


def build_via_mutation(n: int) -> list[int]:  # => in-place mutation: append to the SAME list object
    items: list[int] = []  # => the ONE list object every append() mutates below
    for i in range(n):  # => n updates to the same object
        items.append(i)  # => O(1) amortized -- mutates the existing list in place
    return items  # => the fully-built list


def build_via_persistent_updates(n: int) -> tuple[int, ...]:  # => persistent: each "add" makes a NEW tuple
    items: tuple[int, ...] = ()  # => the starting empty tuple -- rebound, never mutated, on every iteration
    for i in range(n):  # => n updates, but each one is a fresh object
        items = items + (i,)  # => O(k) EVERY time -- copies the whole tuple so far, k = current length
    return items  # => the final tuple, built through n full copies


start = time.perf_counter()  # => wall-clock measurement, not a guess
mutated = build_via_mutation(N)  # => time the in-place mutation approach
mutation_seconds = time.perf_counter() - start  # => elapsed time for the mutation approach

start = time.perf_counter()  # => reset the clock for the second approach
persistent = build_via_persistent_updates(N)  # => time the persistent-update approach
persistent_seconds = time.perf_counter() - start  # => elapsed time for the persistent approach

print(list(mutated) == list(persistent))  # => both approaches are CORRECT -- identical resulting values
# => Output: True
print(mutation_seconds < persistent_seconds)  # => in-place mutation is measurably faster for this workload
# => Output: True
print(f"mutation: {mutation_seconds:.4f}s, persistent: {persistent_seconds:.4f}s")  # => the concrete numbers

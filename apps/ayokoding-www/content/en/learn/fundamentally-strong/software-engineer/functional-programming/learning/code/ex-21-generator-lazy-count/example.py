"""Example 21: A Generator Yields on Demand."""

from typing import Iterator  # => the return type of a generator function


def counter(
    start: int,
) -> Iterator[int]:  # => a generator FUNCTION -- calling it runs NO code yet
    n = start  # => the running value, remembered ACROSS yields
    while (
        True
    ):  # => an INFINITE loop -- safe only because yield pauses execution each time
        yield n  # => pauses here, handing n back to the caller, resuming on the NEXT next()
        n += 1  # => only runs AFTER the caller pulls again


pulled: list[int] = []  # => tracks exactly which values were actually computed
gen = counter(
    10
)  # => creates the generator OBJECT -- the while loop has not run at all yet

pulled.append(
    next(gen)
)  # => resumes the generator until the first yield -- pulled: [10]
pulled.append(next(gen))  # => resumes again from where it paused -- pulled: [10, 11]
pulled.append(next(gen))  # => a third pull -- pulled: [10, 11, 12]

print(pulled)  # => Output: [10, 11, 12]
print(
    len(pulled)
)  # => Output: 3 -- only 3 values ever computed, despite counter() being infinite

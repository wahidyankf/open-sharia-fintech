"""Example 31: Monotonic LSN Assignment."""
# LSNs (Log Sequence Numbers) totally order every WAL record (co-17).


class LsnGenerator:  # => a strictly increasing counter -- the WAL's own clock
    def __init__(self) -> None:  # => starts before any LSN has been issued
        self._next: int = 1  # => LSN 0 is reserved to mean "nothing written yet"

    def next_lsn(
        self,
    ) -> int:  # => issues one new LSN, guaranteed greater than every prior one
        lsn = self._next  # => capture the value about to be issued
        self._next += (
            1  # => strictly increasing: no reuse, no gaps introduced by this generator
        )
        return lsn  # => hand back this call's freshly issued LSN


gen = LsnGenerator()  # => a fresh generator for this example
lsns = [gen.next_lsn() for _ in range(5)]  # => issue five LSNs in a row
print(lsns)  # => Output: [1, 2, 3, 4, 5]

for i in range(1, len(lsns)):  # => walk every consecutive pair
    assert (
        lsns[i] > lsns[i - 1]
    )  # => each new LSN is STRICTLY greater than the previous one
print("ex-31 OK")  # => Output: ex-31 OK

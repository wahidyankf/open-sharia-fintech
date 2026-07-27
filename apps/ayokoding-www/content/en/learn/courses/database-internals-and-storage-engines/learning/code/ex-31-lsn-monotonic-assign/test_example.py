"""Example 31: pytest verification for Monotonic LSN Assignment."""

from example import LsnGenerator


def test_lsns_strictly_increase() -> None:
    gen = LsnGenerator()
    a = gen.next_lsn()
    b = gen.next_lsn()
    c = gen.next_lsn()
    assert a < b < c


def test_two_generators_are_independent() -> None:
    gen1 = LsnGenerator()
    gen2 = LsnGenerator()
    assert (
        gen1.next_lsn() == gen2.next_lsn() == 1
    )  # => each generator starts its own count at 1


# => Run: pytest -- Output: 2 passed

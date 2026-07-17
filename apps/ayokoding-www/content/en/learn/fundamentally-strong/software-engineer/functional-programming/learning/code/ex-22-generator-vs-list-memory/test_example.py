"""Example 22: pytest verification for Generator Expression vs. List."""

import sys


def test_generator_footprint_stays_small() -> None:
    n = 1_000_000
    eager_list = [i * i for i in range(n)]
    lazy_generator = (i * i for i in range(n))
    assert sys.getsizeof(eager_list) > sys.getsizeof(lazy_generator)
    assert sys.getsizeof(lazy_generator) < 300


# => Run: pytest -- Output: 1 passed

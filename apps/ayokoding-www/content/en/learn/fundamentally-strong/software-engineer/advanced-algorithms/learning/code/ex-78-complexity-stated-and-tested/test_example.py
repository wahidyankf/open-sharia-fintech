"""Example 78: pytest verification for Three Stated-and-Tested Complexities."""

from example import binary_search_steps, linear_steps, nlogn_steps


def test_binary_search_steps_grows_logarithmically() -> None:
    assert binary_search_steps(1) == 1  # => a single element: one comparison, done
    assert binary_search_steps(2) == 2
    assert (
        binary_search_steps(1024) == 11
    )  # => ~log2(1024)+1, floor-biased mid rounding


def test_linear_steps_equals_n_exactly() -> None:
    for n in (0, 1, 7, 100):
        assert (
            linear_steps(n) == n
        )  # => O(n) means the count IS n, not just proportional


def test_nlogn_steps_exceeds_plain_linear_for_large_n() -> None:
    n = 512
    assert nlogn_steps(n) > linear_steps(n)  # => n log n outgrows n once log n > 1
    assert nlogn_steps(1) == 0  # => n=1: the inner while never runs (1 < 1 is false)


# => Run: pytest -- Output: 3 passed

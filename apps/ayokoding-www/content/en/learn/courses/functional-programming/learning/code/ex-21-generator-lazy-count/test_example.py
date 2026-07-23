"""Example 21: pytest verification for A Generator Yields on Demand."""

from example import counter


def test_only_pulled_values_are_computed() -> None:
    gen = counter(10)
    pulled = [next(gen), next(gen), next(gen)]
    assert pulled == [10, 11, 12]


# => Run: pytest -- Output: 1 passed

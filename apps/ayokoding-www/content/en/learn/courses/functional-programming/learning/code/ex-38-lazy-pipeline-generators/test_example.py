"""Example 38: pytest verification for A Lazy map/filter Pipeline Pulled by next."""

from typing import Iterator


def test_pipeline_pulls_only_as_many_source_values_as_needed() -> None:
    pulled: list[int] = []

    def source() -> Iterator[int]:
        for n in range(1, 1000):
            pulled.append(n)
            yield n

    doubled = map(lambda n: n * 2, source())
    evens_only = filter(lambda n: n % 4 == 0, doubled)
    result = [next(evens_only), next(evens_only)]
    assert result == [4, 8]
    assert (
        len(pulled) < 10
    )  # => the pipeline never touched most of the 999-element range


# => Run: pytest -- Output: 1 passed

"""Example 23: pytest verification for islice Over an Infinite count()."""

from itertools import count, islice


def test_islice_takes_exactly_n_from_an_infinite_source() -> None:
    infinite_evens = (n for n in count(0, 2))
    first_five = list(islice(infinite_evens, 5))
    assert first_five == [0, 2, 4, 6, 8]
    assert (
        next(infinite_evens) == 10
    )  # => confirms the source resumes right where islice stopped


# => Run: pytest -- Output: 1 passed

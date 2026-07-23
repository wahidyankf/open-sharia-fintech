"""Example 78: pytest verification for A Case Where Laziness Saves Work, and One Where It Hides a Cost."""

from example import lazy_squares, work_done


def test_reiterating_an_exhausted_generator_yields_nothing_silently() -> None:
    work_done.clear()
    stream = lazy_squares(range(1, 4))
    first_pass = list(stream)  # => consumes the generator fully
    assert first_pass == [1, 4, 9]
    assert len(work_done) == 3

    second_pass = list(stream)  # => the SAME (now exhausted) generator object
    assert second_pass == []  # => silently empty -- no error, no recomputation
    assert len(work_done) == 3  # => confirms NOTHING extra was computed


# => Run: pytest -- Output: 1 passed

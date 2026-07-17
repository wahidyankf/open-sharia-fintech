"""Example 51: pytest verification for map and and_then on a Result."""

from typing import Callable

from example import Err, Ok, parse_positive


def test_pipeline_stops_at_the_first_err() -> None:
    times_ten: Callable[[int], int] = lambda n: n * 10
    ok_chain = Ok("5").and_then(parse_positive).map(times_ten)
    err_chain = Ok("-5").and_then(parse_positive).map(times_ten)

    assert ok_chain == Ok(50)
    assert err_chain == Err("-5 is not positive")


# => Run: pytest -- Output: 1 passed

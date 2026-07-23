"""Example 79: pytest verification for The Same Pipeline in Option vs. Result."""

from example import Err, Nothing, Ok, Option, Res, Some, parse_option, parse_result


def _increment_option(n: int) -> Option[int]:
    return Some(n + 1)


def _increment_result(n: int) -> Res[int]:
    return Ok(n + 1)


def test_option_discards_the_reason_result_keeps_it() -> None:
    assert parse_option("bad") == Nothing()
    assert parse_result("bad") == Err("'bad' is not a digit string")
    assert parse_option("5").and_then(_increment_option) == Some(6)
    assert parse_result("5").and_then(_increment_result) == Ok(6)


# => Run: pytest -- Output: 1 passed
